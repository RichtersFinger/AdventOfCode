r"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
"""

# pipe-shape definitions
v = "|"
h = "-"
tl = "F"
tr = "7"
bl = "L"
br = "J"
nopipe = "."


import Base: +
"""
Returns element-wise sum of tuples.
"""
function +(a::Tuple{Int64, Int64}, b::Tuple{Int64, Int64})
    Tuple(v[1] + v[2] for v in zip(a, b))
end
"""
Returns element-wise reversed tuple.
"""
function reverse(a::Tuple{Int64, Int64})
    Tuple(-v for v in a)
end


"""
Returns directions of available exists for given pipe.
"""
function get_exits(pipe)
    if pipe == v
        [(0, -1), (0, 1)]
    elseif pipe == h
        [(-1, 0), (1, 0)]
    elseif pipe == tl
        [(0, -1), (1, 0)]
    elseif pipe == tr
        [(0, -1), (-1, 0)]
    elseif pipe == bl
        [(0, 1), (1, 0)]
    elseif pipe == br
        [(0, 1), (-1, 0)]
    elseif pipe == nopipe
        []
    else
        throw(DomainError(pipe, "unknown pipe"))
    end
end

"""
Returns direction of next pipe from pipe-shape and initial direction.

The type is a tuple of relative indices.
"""
function get_direction(pipe, prev_dir)
    if pipe == v
        if prev_dir == (0, -1) || prev_dir == (0, 1)
            prev_dir
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    elseif pipe == h
        if prev_dir == (1, 0) || prev_dir == (-1, 0)
            prev_dir
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    elseif pipe == tl
        if prev_dir == (0, -1)
            (1, 0)
        elseif prev_dir == (-1, 0)
            (0, 1)
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    elseif pipe == tr
        if prev_dir == (0, -1)
            (-1, 0)
        elseif prev_dir == (1, 0)
            (0, 1)
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    elseif pipe == bl
        if prev_dir == (0, 1)
            (1, 0)
        elseif prev_dir == (-1, 0)
            (0, -1)
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    elseif pipe == br
        if prev_dir == (0, 1)
            (-1, 0)
        elseif prev_dir == (1, 0)
            (0, -1)
        else
            throw(DomainError(string(pipe)*", "*string(prev_dir), "incompatible incoming direction for this pipe"))
        end
    else
        throw(DomainError(pipe, "unknown pipe"))
    end
end

"""
Returns value of array at index-position or nothing if out of bounds
"""
function get_pipe(lines, index)
    if index[1] < 1 || index[1] > length(lines[1]) || index[2] < 1 || index[2] > length(lines)
        return nothing
    end
    return string(lines[index[2]][index[1]])
end


# read input
#s = """..F7.
#.FJ|.
#SJ.L7
#|F--J
#LJ..."""
s = open("input.txt") do file
    read(file, String)
end


# process input into 2d-array
lines = split(s, "\n")
nx = length(lines[1])
ny = length(lines)

# find start
start = nothing
for iy in 1:ny
    ix = findfirst("S", lines[iy])
    if !isnothing(ix)
        global start = (ix[1], iy)
        break
    end
end
if isnothing(start)
    throw(DomainError(start, "No starting position found in input."))
end
println(start)

# find starting dir
current_position = start
start_directions = []
for neighbor in [(-1, 0), (0, -1), (1, 0), (0, 1)]
    index = neighbor + current_position
    pipe = get_pipe(lines, index)
    if !isnothing(pipe) && reverse(neighbor) in get_exits(pipe)
        #println(neighbor)
        push!(start_directions, neighbor)
    end
end
if length(start_directions) != 2
    throw(DomainError(start_directions, "Confusion regarding starting direction in input."))
end
println(
    "Start by following pipes ",
    get_pipe(lines, current_position + start_directions[1]),
    " and ",
    get_pipe(lines, current_position + start_directions[2]),
    " in directions ",
    start_directions
)

# iterate pipe
distance = [0]
current_direction = start_directions[1]
current_position = start
iz = 0
while iz == 0 || current_position != start
    global iz += 1
    global current_position += current_direction
    current_pipe = get_pipe(lines, current_position)
    if current_pipe == "S"
        push!(distance, 0)
    else
        println("next: ", get_pipe(lines, current_position), " at dir ", current_direction, " (dist ", iz, ")")
        global current_direction = get_direction(
            current_pipe,
            current_direction
        )
        push!(distance, iz)
    end
end
# iterate pipe backwards
nz = length(distance)
current_direction = start_directions[2]
current_position = start
iz = 0
while iz == 0 || current_position != start
    global iz += 1
    global current_position += current_direction
    current_pipe = get_pipe(lines, current_position)
    if current_pipe != "S"
        println("next: ", get_pipe(lines, current_position), " at dir ", current_direction, " (dist ", iz, ")")
        global current_direction = get_direction(
            current_pipe,
            current_direction
        )
        distance[nz-iz] = min(distance[nz-iz], iz)
    end
end

println(distance)

println("Maximum distance: ", maximum(distance))