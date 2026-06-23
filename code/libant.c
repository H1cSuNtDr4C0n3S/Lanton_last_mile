#include <stdint.h>
#include <string.h>

/* Langton's ant: white(0) -> turn RIGHT, flip to black, move.
                  black(1) -> turn LEFT,  flip to white, move.
   heading: 0=up(-y), 1=right(+x), 2=down(+y), 3=left(-x)
   turns[t]: 1 = R, 0 = L
   Returns number of steps executed (may stop early at boundary).
   If snap_step >= 0, copies grid and ant state at that step (before executing it).
*/
long simulate(int H,
              const int32_t* xs, const int32_t* ys, long n_cells,
              int ax, int ay, int ah,
              long max_steps,
              uint8_t* turns,
              uint8_t* grid,          /* (2H)*(2H), caller-zeroed */
              long snap_step,
              uint8_t* snap_grid,     /* (2H)*(2H) or NULL */
              int32_t* snap_state)    /* [x,y,h] or NULL */
{
    const int W = 2*H;
    for (long i = 0; i < n_cells; i++) {
        long x = xs[i] + H, y = ys[i] + H;
        if (x < 0 || x >= W || y < 0 || y >= W) continue;
        grid[y*W + x] = 1;
    }
    long x = ax + H, y = ay + H;
    int h = ah;
    static const int dx[4] = {0, 1, 0, -1};
    static const int dy[4] = {-1, 0, 1, 0};
    long t;
    for (t = 0; t < max_steps; t++) {
        if (t == snap_step && snap_grid) {
            memcpy(snap_grid, grid, (size_t)W*W);
            snap_state[0] = (int32_t)(x - H);
            snap_state[1] = (int32_t)(y - H);
            snap_state[2] = (int32_t)h;
        }
        uint8_t c = grid[y*W + x];
        if (c == 0) { h = (h + 1) & 3; grid[y*W + x] = 1; turns[t] = 1; }
        else        { h = (h + 3) & 3; grid[y*W + x] = 0; turns[t] = 0; }
        x += dx[h]; y += dy[h];
        if (x < 1 || x >= W-1 || y < 1 || y >= W-1) return t + 1;
    }
    return t;
}
