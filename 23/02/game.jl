"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
"""

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
