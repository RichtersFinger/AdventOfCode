star = 2 # 1 or 2
output_verbose = false

"""
Returns list of Dict with keys "pos" and "dir" where the ray traveled to.
"""
function follow_ray!(input, output, position, direction, max_depth)
    if max_depth != 0
        x0, y0 = position
        dx, dy = direction
        x1, y1 = (x0 + dx, y0 + dy)
        #println("start ray: $x1, $y1, $max_depth")
        while x1 >= 1 && y1 >= 1 && x1 <= size(input)[1] && y1 <= size(input)[2]
            if Dict("pos" => (x1, y1), "dir" => (dx, dy)) in output
                break
            end
            push!(output, Dict("pos" => (x1, y1), "dir" => (dx, dy)))
            next = input[x1, y1]
            x0, y0 = x1, y1
            if dx != 0
                if next == "|"
                    # spawn second ray
                    follow_ray!(input, output, (x0, y0), (dy, dx), max_depth - 1)
                    dx, dy = dy, -dx
                elseif next == "/"
                    dx, dy = dy, -dx
                elseif next == "\\"
                    dx, dy = dy, dx
                end
            elseif dy != 0
                if next == "-"
                    # spawn second ray
                    follow_ray!(input, output, (x0, y0), (dy, dx), max_depth - 1)
                    dx, dy = -dy, dx
                elseif next == "/"
                    dx, dy = -dy, dx
                elseif next == "\\"
                    dx, dy = dy, dx
                end
            end
            x1, y1 = x0 + dx, y0 + dy
        end
    end
    return output
end

# read input
s = open("input.txt") do file
    read(file, String)
end

# process input into 2d-array
sl = split(s, "\n")
sa = ["$(sl[y][x])" for x ∈ eachindex(sl[1]), y ∈ eachindex(sl)]

result = -1
if star == 1
    # perform analysis
    energization_raw = follow_ray!(sa, [], (0, 1), (1, 0), -1)
    global result = length(unique!([e["pos"] for e in energization_raw]))

    if output_verbose
        # format result
        energization = fill(".", length(sl[1]), length(sl))
        for e in energization_raw
            energization[e["pos"][1], e["pos"][2]] = "#"
        end
        energization_str = join((join(energization[:, y]) for y in eachindex(sl)), "\n")
        println(energization_str)
    end
elseif star == 2
    nx = length(sl[1])
    ny = length(sl)
    for y in 1:ny
        energization_raw = follow_ray!(sa, [], (0, y), (1, 0), -1)
        global result = max(result, length(unique!([e["pos"] for e in energization_raw])))
        println("$y, $result")
    end
    for y in 1:ny
        energization_raw = follow_ray!(sa, [], (nx+1, y), (-1, 0), -1)
        global result = max(result, length(unique!([e["pos"] for e in energization_raw])))
        println("$y, $result")
    end
    for x in 1:nx
        energization_raw = follow_ray!(sa, [], (x, 0), (0, 1), -1)
        global result = max(result, length(unique!([e["pos"] for e in energization_raw])))
        println("$x, $result")
    end
    for x in 1:nx
        energization_raw = follow_ray!(sa, [], (x, ny+1), (0, -1), -1)
        global result = max(result, length(unique!([e["pos"] for e in energization_raw])))
        println("$x, $result")
    end
else
    println("what?")
end

# output result
println("number of energized fields: $result")
