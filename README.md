Our Implementation of Monte Carlo Tree Search as seen in mcts_vanilla.py was able to beat a simple rollout algorithm 80% of the time when utilizing a 1000 node search tree

For Experiment 1, we ran the mcts_vanilla against itself at different tree sizes: 100 vs 100, 100 vs 500, 100 vs 1000, and 100 vs 10000. Each bout was conducted over 100 matches and we gathered the win rates and the time taken for each. As expected when both bots have the same number of nodes (100 vs 100) the games were very even and the overall scores were split 48/52. It was a very quick calculation as well taking only 202.8 seconds. As the node disparity increased the matches got skewed very quickly towards the bot with the larger search tree. (100 vs 500) concluded with 18 to 82 in favor of the 500 node tree, over a period of 577.2 seconds. (100 vs 1000) concluded with a staggering 3 to 97 in favor of the 1000 node tree, however it took 1179.6 seconds. The largest test we ran was (100 vs 10000) which took a lengthy 9168.9 seconds or over 2.5 hours to run and concluded with 88 for 10000 and 12 for 100. This data shows that more nodes does in fact cause an increase in win rate.

Our heuristic improvement was rather simple - we had the MCTS bot pick an open center square as an action to run a simulated game against before choosing any other squares.If it found another square that was open that offered a better win chance, then it could still take that square, but this bot should slightly favor center squares in general. Overall the results were not particularly favorable for our heuristic. We played four games and the heuristic bot did not ever win more often than our vanilla bot, however the results were often quite close, near 50/50.

Our first test was a tree size of 100 vs 100, and our vanilla bot defeated our modified bot 55 times compared to 45. The time taken was 209 seconds.

Our second test was of size 200 vs 200, and our vanilla bot won 53 times compared to 47 times for our modified bot. The time taken was more than double at 473 seconds.

Our third test was of size 500 vs 500, and the gap closed. Vanilla won 51 times compared to modified winning 49 times, taking 1,114 seconds to complete.

And finally our fourth test was of size 1000 vs 1000, and the two bots performed perfectly evenly, both coming out to 50 wins. Time taken was 2,281 seconds.

It seems that as the node count increased, the heuristic made less and less of an impact on the decisions that were made by our modified bot until at a certain point it was behaving functionally the same as our vanilla mcts bot.


For fun we also did a single test where we reversed the heuristic and made our modified bot favor squares that were not the center, however doing so, interestingly, made our modified bot lose at a significantly higher rate.

The results of our 100 vs 100 test were 64 wins for our vanilla and 36 for our heuristic.
