"""
移动机器人运动规划示例：A* 全局规划 + DWA 局部规划（差速底盘）

依赖：numpy、matplotlib（保存 GIF 还需要 pillow）
    pip install numpy matplotlib pillow

运行：
    python astar_dwa.py          # 弹窗实时显示动画
    python astar_dwa.py --save   # 保存为 astar_dwa.gif 和 astar_dwa.png
"""
import argparse
import heapq
import math

import numpy as np
import matplotlib

# ============================================================
# 1. 地图
# ============================================================
RES = 0.25  # 每个栅格的边长（米）


def make_map(w=60, h=40):
    """返回栅格地图 grid[y, x]，True 表示障碍物。地图尺寸为 15m x 10m。"""
    grid = np.zeros((h, w), dtype=bool)
    grid[0, :] = grid[-1, :] = grid[:, 0] = grid[:, -1] = True  # 外墙
    grid[0:28, 15:17] = True   # 墙 1（从下往上，上方留出通道）
    grid[12:40, 30:32] = True  # 墙 2（从上往下，下方留出通道）
    grid[0:28, 45:47] = True   # 墙 3
    grid[30:33, 38:41] = True  # 一个方块障碍物
    grid[18:22, 22:25] = True  # 另一个方块障碍物
    return grid


def inflate(grid, r):
    """膨胀障碍物：把机器人半径加到障碍物上，之后就能把机器人当作点来规划。"""
    h, w = grid.shape
    out = grid.copy()
    ys, xs = np.nonzero(grid)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                out[np.clip(ys + dy, 0, h - 1), np.clip(xs + dx, 0, w - 1)] = True
    return out


def world_to_cell(p):
    return int(p[0] / RES), int(p[1] / RES)


def cell_to_world(c):
    return (c[0] + 0.5) * RES, (c[1] + 0.5) * RES


# ============================================================
# 2. A* 全局规划（8 邻域）
# ============================================================
def astar(grid, start, goal):
    """在栅格上做 A* 搜索。start/goal 为 (x, y) 栅格坐标。
    返回 (路径栅格列表, 已扩展节点集合)；找不到路径时路径为 None。"""
    h, w = grid.shape
    s2 = math.sqrt(2)
    moves = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1),
             (1, 1, s2), (1, -1, s2), (-1, 1, s2), (-1, -1, s2)]

    def heuristic(a):  # 启发函数：欧氏距离（可采纳，保证最优）
        return math.hypot(a[0] - goal[0], a[1] - goal[1])

    open_list = [(heuristic(start), start)]
    g = {start: 0.0}
    parent = {start: None}
    closed = set()

    while open_list:
        _, cur = heapq.heappop(open_list)
        if cur in closed:
            continue
        if cur == goal:  # 回溯得到路径
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], closed
        closed.add(cur)

        for dx, dy, cost in moves:
            nx, ny = cur[0] + dx, cur[1] + dy
            if not (0 <= nx < w and 0 <= ny < h) or grid[ny, nx]:
                continue
            # 禁止斜着"切角"穿过障碍物
            if dx and dy and (grid[cur[1], nx] or grid[ny, cur[0]]):
                continue
            ng = g[cur] + cost
            if ng < g.get((nx, ny), math.inf):
                g[(nx, ny)] = ng
                parent[(nx, ny)] = cur
                heapq.heappush(open_list, (ng + heuristic((nx, ny)), (nx, ny)))
    return None, closed


# ============================================================
# 3. DWA 局部规划
# ============================================================
class Config:
    max_v = 1.0          # 最大线速度 m/s
    min_v = 0.0          # 最小线速度（不允许倒车）
    max_w = 2.0          # 最大角速度 rad/s
    max_acc = 1.0        # 最大线加速度 m/s^2
    max_dw = 3.0         # 最大角加速度 rad/s^2
    v_res = 0.02         # 线速度采样分辨率
    w_res = 0.05         # 角速度采样分辨率
    dt = 0.1             # 控制周期 s
    predict_time = 2.0   # 前向模拟时长 s
    robot_radius = 0.3   # 机器人半径 m
    lookahead = 1.5      # 局部目标点在全局路径上的前视距离 m
    # 代价函数权重（代价越小越好）
    w_goal = 1.0         # 轨迹终点到局部目标的距离
    w_heading = 0.3      # 终点朝向与局部目标方向的夹角
    w_speed = 0.5        # 鼓励走得快
    w_obs = 0.3          # 远离障碍物


def predict_trajectory(state, v, w, cfg):
    """以恒定 (v, w) 前向模拟，返回 [N, 3] 的轨迹 (x, y, theta)。"""
    n = int(cfg.predict_time / cfg.dt)
    traj = np.empty((n + 1, 3))
    x, y, th = state[0], state[1], state[2]
    traj[0] = (x, y, th)
    for i in range(1, n + 1):
        th += w * cfg.dt
        x += v * math.cos(th) * cfg.dt
        y += v * math.sin(th) * cfg.dt
        traj[i] = (x, y, th)
    return traj


def dwa_control(state, local_goal, obstacles, cfg):
    """state = [x, y, theta, v, w]。返回最优 (v, w) 及其预测轨迹。"""
    x, y, _, v0, w0 = state
    # 动态窗口：当前速度在一个控制周期内能达到的速度范围
    vs = np.arange(max(cfg.min_v, v0 - cfg.max_acc * cfg.dt),
                   min(cfg.max_v, v0 + cfg.max_acc * cfg.dt) + 1e-9, cfg.v_res)
    ws = np.arange(max(-cfg.max_w, w0 - cfg.max_dw * cfg.dt),
                   min(cfg.max_w, w0 + cfg.max_dw * cfg.dt) + 1e-9, cfg.w_res)

    # 只考虑附近的障碍物，提高速度
    near = obstacles[np.hypot(obstacles[:, 0] - x, obstacles[:, 1] - y) < 4.0]

    best_cost, best_u, best_traj = math.inf, (0.0, 0.0), None
    for v in vs:
        for w in ws:
            traj = predict_trajectory(state, v, w, cfg)

            # 障碍物代价：轨迹上离障碍物的最小距离
            if len(near):
                d = np.hypot(traj[:, 0, None] - near[None, :, 0],
                             traj[:, 1, None] - near[None, :, 1]).min()
            else:
                d = math.inf
            if d <= cfg.robot_radius:  # 会碰撞，直接淘汰
                continue
            obs_cost = 1.0 / d

            ex, ey, eth = traj[-1]
            goal_cost = math.hypot(local_goal[0] - ex, local_goal[1] - ey)
            ang = math.atan2(local_goal[1] - ey, local_goal[0] - ex) - eth
            heading_cost = abs(math.atan2(math.sin(ang), math.cos(ang)))
            speed_cost = cfg.max_v - v

            cost = (cfg.w_goal * goal_cost + cfg.w_heading * heading_cost
                    + cfg.w_speed * speed_cost + cfg.w_obs * obs_cost)
            if cost < best_cost:
                best_cost, best_u, best_traj = cost, (v, w), traj

    # 恢复行为：所有候选都会碰撞，或者机器人停住了 → 原地朝局部目标转
    if best_traj is None or (abs(best_u[0]) < 1e-3 and abs(best_u[1]) < 1e-3):
        ang = math.atan2(local_goal[1] - y, local_goal[0] - x) - state[2]
        ang = math.atan2(math.sin(ang), math.cos(ang))
        best_u = (0.0, math.copysign(cfg.max_w * 0.5, ang))
        best_traj = predict_trajectory(state, *best_u, cfg)
    return best_u, best_traj


def find_local_goal(path, pos, last_idx, lookahead):
    """在全局路径上找机器人最近的点，再往前取 lookahead 距离作为局部目标。"""
    seg = path[last_idx:]
    idx = last_idx + int(np.argmin(np.hypot(seg[:, 0] - pos[0], seg[:, 1] - pos[1])))
    j, dist = idx, 0.0
    while j < len(path) - 1 and dist < lookahead:
        dist += np.hypot(*(path[j + 1] - path[j]))
        j += 1
    return path[j], idx


# ============================================================
# 4. 主程序：规划 + 仿真 + 可视化
# ============================================================
def main(save=False):
    if save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import animation
    from matplotlib.patches import Circle

    cfg = Config()
    grid = make_map()
    h, w = grid.shape
    start, goal = (1.0, 1.0), (14.0, 1.5)

    # ---- 全局规划：在膨胀后的地图上跑 A* ----
    inflated = inflate(grid, int(math.ceil((cfg.robot_radius + 0.1) / RES)))
    cell_path, explored = astar(inflated, world_to_cell(start), world_to_cell(goal))
    if cell_path is None:
        print("A* 未找到路径")
        return
    path = np.array([cell_to_world(c) for c in cell_path])
    path_len = np.sum(np.hypot(*np.diff(path, axis=0).T))
    print(f"A* 扩展节点数: {len(explored)}，路径长度: {path_len:.2f} m")

    # ---- 局部规划：DWA 跟踪全局路径 ----
    obstacles = np.array([cell_to_world((x, y)) for y, x in zip(*np.nonzero(grid))])
    state = np.array([start[0], start[1], 0.0, 0.0, 0.0])
    history, preds, lgoals = [state.copy()], [], []
    idx = 0
    for step in range(3000):
        local_goal, idx = find_local_goal(path, state[:2], idx, cfg.lookahead)
        (v, wv), traj = dwa_control(state, local_goal, obstacles, cfg)
        # 用运动模型更新机器人状态
        state[2] += wv * cfg.dt
        state[0] += v * math.cos(state[2]) * cfg.dt
        state[1] += v * math.sin(state[2]) * cfg.dt
        state[3], state[4] = v, wv
        history.append(state.copy())
        preds.append(traj)
        lgoals.append(local_goal)
        if math.hypot(state[0] - goal[0], state[1] - goal[1]) < 0.3:
            print(f"到达目标！用时 {step * cfg.dt:.1f} s")
            break
    else:
        print("超出最大步数，未到达目标")
    history = np.array(history)

    # ---- 可视化 ----
    fig, ax = plt.subplots(figsize=(10, 7))
    extent = [0, w * RES, 0, h * RES]
    show = np.zeros((h, w))
    show[inflated] = 0.35   # 膨胀区域：浅灰
    show[grid] = 1.0        # 障碍物：黑
    ax.imshow(show, cmap="Greys", origin="lower", extent=extent, vmin=0, vmax=1)
    ex = np.array([cell_to_world(c) for c in explored])
    ax.scatter(ex[:, 0], ex[:, 1], s=2, c="#9ecae1", alpha=0.5, label="A* explored")
    ax.plot(path[:, 0], path[:, 1], "--", c="#3182bd", lw=1.5, label="A* global path")
    ax.plot(*start, "go", ms=10, label="start")
    ax.plot(*goal, "r*", ms=15, label="goal")

    trail, = ax.plot([], [], "-", c="#e6550d", lw=2, label="robot trajectory")
    pred_line, = ax.plot([], [], "-", c="#31a354", lw=2, label="DWA prediction")
    lg_dot, = ax.plot([], [], "mx", ms=10, mew=2, label="local goal")
    body = Circle((0, 0), cfg.robot_radius, fc="#fdae6b", ec="#e6550d", lw=1.5, zorder=5)
    ax.add_patch(body)
    heading, = ax.plot([], [], "k-", lw=2, zorder=6)
    info = ax.text(0.2, h * RES - 0.5, "", fontsize=10, va="top",
                   bbox=dict(fc="white", alpha=0.8))
    ax.set_xlim(extent[:2])
    ax.set_ylim(extent[2:])
    ax.set_aspect("equal")
    ax.set_title("A* global planning + DWA local planning")
    ax.legend(loc="upper right", fontsize=8, ncol=2)

    frames = range(0, len(preds), 2)

    def update(k):
        s = history[k]
        trail.set_data(history[:k + 1, 0], history[:k + 1, 1])
        pred_line.set_data(preds[k][:, 0], preds[k][:, 1])
        lg_dot.set_data([lgoals[k][0]], [lgoals[k][1]])
        body.center = (s[0], s[1])
        heading.set_data([s[0], s[0] + 0.45 * math.cos(s[2])],
                         [s[1], s[1] + 0.45 * math.sin(s[2])])
        info.set_text(f"t = {k * cfg.dt:4.1f} s   v = {history[k + 1, 3]:.2f} m/s"
                      f"   w = {history[k + 1, 4]:+.2f} rad/s")
        return trail, pred_line, lg_dot, body, heading, info

    anim = animation.FuncAnimation(fig, update, frames=frames, interval=40, blit=False)
    if save:
        anim.save("astar_dwa.gif", writer=animation.PillowWriter(fps=25))
        update(len(preds) - 1)
        fig.savefig("astar_dwa.png", dpi=120, bbox_inches="tight")
        print("已保存 astar_dwa.gif 和 astar_dwa.png")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="保存为 GIF/PNG 而不是弹窗显示")
    main(save=parser.parse_args().save)