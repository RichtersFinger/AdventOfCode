"""
Convert strings like "X blue, Y red, Z green" into Integer tuple.
"""
function separate_rgb(s)
    s_red = match(r"([0-9]*)( red)", s)
    s_green = match(r"([0-9]*)( green)", s)
    s_blue = match(r"([0-9]*)( blue)", s)

    if isnothing(s_red)
        red = 0
    else
        red = parse(Int64, s_red[1])
    end
    if isnothing(s_green)
        green = 0
    else
        green = parse(Int64, s_green[1])
    end
    if isnothing(s_blue)
        blue = 0
    else
        blue = parse(Int64, s_blue[1])
    end

    (red, green, blue)
end

"""
Check whether game (list of rgb-tuples) is compatible with specific bag content (rgb-tuple).
"""
function validate_game(game, rgb)
    for _rgb in game
        for i in 1:3
            if _rgb[i] > rgb[i]
                return false
            end
        end
    end

    true
end

"""
Get minimum content (rgb-tuple) for given game (list of rgb-tuples).
"""
function min_game(game)
    r = 0
    g = 0
    b = 0
    for _rgb in game
        if _rgb[1] > r
            r = _rgb[1]
        end
        if _rgb[2] > g
            g = _rgb[2]
        end
        if _rgb[3] > b
            b = _rgb[3]
        end
    end
    (r, g, b)
end

"""
Get the power of some bag content (rgb-tuple).
"""
function content_power(rgb)
    rgb[1]*rgb[2]*rgb[3]
end

# read input
s = open("input.txt") do file
    read(file, String)
end

# process input into list of lists of rgb-tuples
games_str = split(s, "\n")
games = []
for line in games_str
    game_str = split(line, ":")[2]

    game = []
    for it in split(game_str, ";")
        push!(game, separate_rgb(it))
    end
    #print(game_str*"\n")
    #print(string(game)*"\n")

    push!(games, game)
end

# test for games that are possible if rgb=(12, 13, 14)
rgb = (12, 13, 14)
valid_games = []
for (i, game) in enumerate(games)
    if validate_game(game, rgb)
        push!(valid_games, i)
    end
end
println("Sum of possible games: "*string(sum(valid_games)))

# find power for minimum sets
powers = [content_power(min_game(game)) for game in games]
println("Sum of powers of games: "*string(sum(powers)))

#print(games)
