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