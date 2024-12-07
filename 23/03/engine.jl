r"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

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
