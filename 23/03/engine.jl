"""
Returns true if input string is digit.
"""
function is_digit(chr)
    chr ∈ [string(i) for i in 0:9]
end
"""
Returns true if input string is neither a digit nor a dot.
"""
function is_symbol(chr)
    chr ≠ "." && !(is_digit(chr))
end
"""
Set index and its eight neighbors of array to value
"""
function set_value_and_neighbors(ix, iy, array, value)
    array[
        max(1, ix - 1):min(size(array, 1), ix + 1),
        max(1, iy - 1):min(size(array, 2), iy + 1)
    ] .= value
end

# read input
s = open("input.txt") do file
    read(file, String)
end

# process input into 2d-array and mark engine parts via bool-array
lines = split(s, "\n")
nx = length(lines[1])
ny = length(lines)
engine_bool = falses((nx, ny))
for (iy, line) in enumerate(lines)
    for (ix, chr) in enumerate(line)
        if is_symbol(string(chr))
            set_value_and_neighbors(ix, iy, engine_bool, true)
        end
    end
end
#for iy in 1:ny
#    println(engine_bool[:, iy])
#end

# reprocess and search for relevant numbers
numbers = []
for (iy, line) in enumerate(lines)
    current_number = ""
    relevant_part = false
    for (ix, chr) in enumerate(line)
        if is_digit(string(chr))
            # append digits to number
            current_number *= chr
            relevant_part = relevant_part || engine_bool[ix, iy]
        else
            # evaluate and reset
            if relevant_part
                push!(numbers, parse(Int, current_number))
            end
            current_number = ""
            relevant_part = false
        end
    end
    if relevant_part
        push!(numbers, parse(Int, current_number))
    end
end

println(numbers)

println("Sum of parts: "*string(sum(numbers)))
