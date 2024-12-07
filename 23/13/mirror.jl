"""
Returns transposed multi-line string.
"""
function transpose(a)
    al = split(a, "\n")
    nx = length(al[1])
    ny = length(al)
    r = Array{Char, 2}(undef, (nx, ny))
    for i in 1:nx
        for j in 1:ny
            r[i, j] = al[j][i]
        end
    end
    join([join(r[i, :], "") for i in 1:nx], "\n")
end

"""
Returns position of first horizontal mirror-line.
"""
function mirror_line(a)
    #println("pattern:\n$a")
    al = split(a, "\n")
    ny = length(al)
    for i in 1:ny-1
        if al[i] == al[i + 1]
            #println("maybe: $i-$(i+1)")
            # this is a candidate
            mirror = true
            for j in 1:min(i - 1, ny - i - 1)
                #println("check: $(i-j)-$(i + 1 + j)")
                if al[i-j] != al[i + 1 + j]
                    mirror = false
                    break
                end
            end
            if mirror
                #println("YES: $i-$(i+1)\n")
                return i
            end
        end
    end
    #println("\n")
    return 0
end

# read input
s = open("input.txt") do file
    read(file, String)
end


# process input into 2d-array
blocks = split(s, "\n\n")

result = sum(100*mirror_line(block) for block in blocks) + sum(mirror_line(transpose(block)) for block in blocks)

println("Result: $result")
