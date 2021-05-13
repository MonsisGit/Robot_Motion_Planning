#include <iostream>
#include <experimental/random>
#include <math.h>

int *create_grid(int, int);
void print_grid(int *, int, int);
int *dilation(int *, int *, int, bool = true, int = 1);
int *spawn_obstacles(int *, int, int, int);
int *add_non_ones(int *, int *, int, bool, int);
int *create_border(int *, int, int);
int *brushfire(int *, int, int);
bool detect_zeros(int *, int);
int *get_skeleton(int *, int, int);

void print_grid(int *grid, int row, int col)
{
    std::cout << "The array looks like this:\n";
    int i, j;
    for (i = 0; i < row; i++)
    {
        for (j = 0; j < col; j++)
        {
            if (grid[j + i * col] < 10)
            {
                std::cout << grid[j + i * col] << "  ";
            }
            else
            {
                std::cout << grid[j + i * col] << " ";
            }
        }
        std::cout << "\n";
    }
}

int *create_array(int row, int col)
{
    int *grid = new int[row * col];
    //std::cout << "created grid of size: (" << row << ", " << col << ")\n";
    return grid;
}

int *dilation(int *grid, int kernel_size, int row, int col, bool set_to_one, int dil_count)
{
    //int k_col = col-floor(kernel_size/2);
    //int k_row = row-floor(kernel_size/2);
    int *grid_dilated = create_array(row, col);

    for (int i = 1; i < row; i++)
    {
        for (int j = 1; j < col; j++)
        {
            for (int k_x = -1; k_x < 2; k_x++)
            {
                for (int k_y = -1; k_y < 2; k_y++)
                {
                    int ker_pos = j + i * col + (k_x * col + k_y);
                    if (grid[ker_pos] != 0 && grid[j + i * col] == 0)
                    {
                        grid_dilated[j + i * col] = dil_count;
                    }
                }
                //std::cout<<"\n";
            }
        }
    }
    grid = add_non_ones(grid, grid_dilated, row * col, set_to_one, dil_count);
    return grid;
}

int *add_non_ones(int *grid, int *grid_dilated, int length, bool set_to_one, int dil_count)
{
    for (int i = 0; i < length; i++)
    {
        if (set_to_one && grid[i] + grid_dilated[i] > 0)
        {
            grid[i] = 1;
        }
        else
        {
            if (grid_dilated[i] == dil_count)
            {
                grid[i] = grid_dilated[i];
            }
        }
    }
    return grid;
}

int *spawn_obstacles(int *grid, int row, int col, int nm_obstacles)
{
    int rand_nm = std::experimental::randint(3, nm_obstacles);
    std::cout << "number of obstacles: " << rand_nm << "\n";
    for (int i = 0; i < rand_nm; ++i)
    {
        grid[std::experimental::randint(0, row * col)] = 1;
    }
    for (int j = 0; j < 2; j++)
    {
        grid = dilation(grid, 3, row, col, true, 1);
    }
    grid = create_border(grid, row, col);
    return grid;
}

int *create_border(int *grid, int row, int col)
{
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < col; j++)
        {
            if (i == 0 || i == row - 1)
            {
                grid[j + i * col] = 1;
            }
            if (j == 0 || j == col - 1)
            {
                grid[j + i * col] = 1;
            }
        }
    }
    return grid;
}

bool detect_zeros(int *grid, int length)
{
    for (int i = 0; i < length; i++)
    {
        if (grid[i] == 0)
        {
            return true;
        }
    }
    return false;
}

int *get_skeleton(int *grid, int length, int nm_iter)
{
    for (int i = 0; i < length; i++)
    {
        if (grid[i] != 1 && grid[i] != nm_iter)
        {
            grid[i] = 0;
        }
    }
    return grid;
}

int *brushfire(int *grid, int row, int col)
{
    for (int i = 2; i < col; i++)
    {
        grid = dilation(grid, 4, row, col, false, i);
        if ((detect_zeros(grid, row * col)) == false)
        {
            //grid = get_skeleton(grid, row * col, i);
            break;
        }
    }
    return grid;
}

int main()
{
    const int row = 30;
    const int col = 30;
    int nm_obstacles = 6;
    int *grid = create_array(row, col);
    int *obst_grid = spawn_obstacles(grid, row, col, nm_obstacles);
    //print_grid(obst_grid, row, col);
    int *bf_grid = brushfire(obst_grid, row, col);
    print_grid(grid, row, col);
    delete[] bf_grid, obst_grid, grid;
    return 0;
}
