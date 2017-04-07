using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading;

namespace FallingRocks
{
    public class Dwarf
    {
        private const ushort Row = 18; // Where Hero is

        public char icon = 'O';
        public int score = 0;
        private int x = 15;
        Thread moveDwarfThread;

        public Dwarf()
        {
            Console.SetCursorPosition(x, Row);
            Console.Write(icon);
        }

        public int X
        {
            get { return x; }
            set { x = value; }
        }

        public bool Dead { get; set; }

        public void MoveDwarf()
        {
            moveDwarfThread = new Thread(CreateMovementThread);
            moveDwarfThread.Start();
        }

        private void CreateMovementThread()
        {
            while (!Dead)
            {
                ConsoleKeyInfo keyInfo = Console.ReadKey();
                if (keyInfo.Key == ConsoleKey.LeftArrow)
                {
                    Console.SetCursorPosition(x, Row);
                    Console.Write(" ");
                    if (x == 1)
                    {
                        Console.SetCursorPosition(x, Row); // We are at the edge and can't                    
                    }                                      // move any farther
                    else
                    {
                        x--;
                    }
                    Console.SetCursorPosition(x, Row);
                    Console.Write(icon);
                }
                else if (keyInfo.Key == ConsoleKey.RightArrow)  // There's a weird glitch when Hero
                {                                               // gets close to the right side,
                    if (x == Console.BufferWidth - 3)           // so I had to prevent him from going
                    {                                           // there in the first place
                        Console.SetCursorPosition(x - 2, Row);
                    }
                    else
                    {
                        Console.SetCursorPosition(x, Row);
                        Console.Write(" ");
                        x++;
                    }
                    Console.SetCursorPosition(x, Row);
                    Console.Write(icon);
                }
            }
        }

        public void MoveWithAgent(int action)
        {
            if (action == 0)
            {
                Console.SetCursorPosition(x, Row);
                Console.Write(" ");
                if (x == 1)
                {
                    Console.SetCursorPosition(x, Row);
                }
                else
                {
                    x--;
                }
                Console.SetCursorPosition(x, Row);
                Console.Write(icon);
            }
            else if (action == 2)
            {
                if (x == Console.BufferWidth - 3)
                {
                    Console.SetCursorPosition(x - 2, Row);
                }
                else
                {
                    Console.SetCursorPosition(x, Row);
                    Console.Write(" ");
                    x++;
                }
                Console.SetCursorPosition(x, Row);
                Console.Write(icon);
            }
        }

        public int TrackScore(DateTime start, DateTime end)
        {
            TimeSpan timeElapsed = start - end;
            score = (int)timeElapsed.TotalSeconds;
            return Math.Abs(score);
        }
    }

    [Serializable]
    public class Rock
    {
        public char[] rockType =
            new char[] { '^', '@', '*', '&', '+', '%', '$', '#', '!', '.', ';', '-' };
        List<List<Rock>> allRows = new List<List<Rock>>();
        public int x;
        public int y;
        public char type;
        public Random rockCount = new Random();
        public Random chooseType = new Random();
        public Random initialX = new Random();

        public Rock()
        {
            x = initialX.Next(1, 28);
            y = 0;
            type = rockType[chooseType.Next(0, 12)];
            Console.SetCursorPosition(x, y);
        }

        public List<Rock> InitializeRow()
        {
            List<Rock> rocks = new List<Rock>();
            int count = rockCount.Next(1, 5);

            for (int i = 0; i < count; i++)
            {
                rocks.Add(new Rock());
                Thread.Sleep(10);
            }

            return rocks;
        }
        
        public bool ReignChaos(int heroPosition)
        {
            bool gameOver = false;

            allRows.Add(InitializeRow());

            if (allRows.Count > 21)
            {
                allRows.RemoveAt(0);
            }

            foreach (List<Rock> row in allRows)
            {
                foreach (Rock rock in row)
                {
                    gameOver = GameIsOver(rock, heroPosition);

                    if (rock.y != 0) 
                    {
                        Console.SetCursorPosition(rock.x, rock.y - 1);
                        Console.Write(" ");
                    }

                    if (rock.y == Console.BufferHeight)
                    {
                        Console.SetCursorPosition(rock.x, 0);
                    }
                    else
                    {
                        Console.SetCursorPosition(rock.x, rock.y);
                        Console.Write(rock.type);
                        rock.y++;
                    }

                    if (gameOver)
                    {
                        Console.SetCursorPosition(rock.x, rock.y - 1);
                        Console.Write("X");

                        return gameOver;
                    }
                }
            }

            return gameOver;
        }

        public List<List<Rock>> GetNextState()
        {
            var simulatedRows = new List<List<Rock>>(MakeDeepCopy(allRows));

            foreach (List<Rock> row in simulatedRows)
            {
                foreach (Rock rock in row)
                {
                    rock.y++;
                }
            }

            return simulatedRows;
        }

        public double[] GetStateFeatures(int heroX)
        {
            double[] features = new double[28 * 18];

            for (int row = 0; row < this.allRows.Count; row++)
            {
                for (int rockId = 0; rockId < this.allRows[row].Count; rockId++)
                {
                    var rock = this.allRows[row][rockId];

                    if (rock.y >= 18)
                    {
                        continue;
                    }

                    double feature = ((double)(rock.y - 18) / (rock.x * heroX));
                    features[rock.y * 28 + rock.x] = feature;
                }
            }

            return features;
        }

        public static bool GameIsOver(Rock rock, int heroPosition)
        {
            return (rock.y == 18 && rock.x == heroPosition);
        }

        internal static T MakeDeepCopy<T>(T obj)
        {
            using (MemoryStream ms = new MemoryStream())
            {
                BinaryFormatter formatter = new BinaryFormatter();

                formatter.Serialize(ms, obj);

                ms.Position = 0;

                return (T)formatter.Deserialize(ms);
            }
        }
    }

    class Battlefield
    {
        public Battlefield()
        {
            Console.Clear();

            Console.WindowHeight = 20;
            Console.BufferHeight = 20;
            Console.WindowWidth = 30;
            Console.BufferWidth = 30;
            Console.CursorVisible = false;
        }
    }

    class GameInitialization
    {
        static void Main()
        {
            Agent agent = new Agent(28, 18);
            int episodes = 10000;
            int currentEpisode = 0;

            while (currentEpisode < episodes)
            {
                Battlefield battlefield = new Battlefield();
                Dwarf hero = new Dwarf();
                Rock rock = new Rock();

                while (true) // Episodic semi-gradient SARSA for control, chapter 10
                {
                    double[] features = rock.GetStateFeatures(hero.X);
                    double[] gradient = features;
                    agent.SimulatedNextState = rock.GetNextState();
                    int action = agent.GetAction(hero.X, features); 

                    hero.MoveWithAgent(action); // Take A

                    if (rock.ReignChaos(hero.X)) // Observe R, S'
                    {
                        hero.Dead = true;

                        agent.UpdateWeights(0, null, gradient); // Update weights when terminal

                        break;
                    }

                    int bestAction = agent.GetAction(hero.X, rock.GetStateFeatures(hero.X), true); // Choose A'
                    int newHeroPos = (bestAction == 0) ? hero.X - 1 : (bestAction == 1) ? hero.X : hero.X + 1; 
                    double[] newStateFeatures = rock.GetStateFeatures(newHeroPos); // Get the new state features given A' and S'

                    agent.UpdateWeights(1, newStateFeatures, gradient); // Update weights given A' and S' // DIVERGES, but is the correct way to implement
                    //agent.UpdateWeights(1, rock.GetStateFeatures(hero.X), gradient); // Update weights given A' and S' // DOES NOT DIVERGE, but is the incorrect way

                    //Thread.Sleep(150);
                }

                currentEpisode++;
            }
        }
    }
}