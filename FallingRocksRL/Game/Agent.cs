namespace FallingRocks
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    public class Agent
    {
        private const double alpha = 0.01;
        private const double gamma = 0.9;

        private double[] theta;
        private int fieldWidth;
        private double oldActionValue;

        public Agent(int fieldWidth, int fieldHeight)
        {
            this.theta = new double[fieldWidth * fieldHeight];
            this.fieldWidth = fieldWidth;
        }

        public List<List<Rock>> SimulatedNextState { get; set; }

        public int GetAction(int y, double[] phi)
        {
            //double epsilon = 0.1;
            //Random rand = new Random();

            //if (rand.NextDouble() < epsilon)
            //{
            //    return rand.Next(0, 3);
            //}

            int left = (y - 1) >= 0 ? y - 1 : y;
            int doNothing = y;
            int right = (y + 1) < fieldWidth ? y + 1 : y;
            this.oldActionValue = this.GetActionValue(phi);
            double[] actionValues = new double[]
            {
                GetActionValue(this.GetNextStateFeatures(left)),
                GetActionValue(this.GetNextStateFeatures(doNothing)),
                GetActionValue(this.GetNextStateFeatures(right))
            };
            double maxAction = actionValues.Max();
            int action = Array.IndexOf(actionValues, maxAction);

            return action;
        }

        public double[] GetNextStateFeatures(int heroX)
        {
            double[] features = new double[28 * 18];

            for (int row = 0; row < this.SimulatedNextState.Count; row++)
            {
                for (int rockId = 0; rockId < this.SimulatedNextState[row].Count; rockId++)
                {
                    var rock = this.SimulatedNextState[row][rockId];

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

        public void UpdateWeights(int reward, double[] newPhi, double[] gradient)
        {
            double newActionValue = this.GetActionValue(newPhi);

            for (int i = 0; i < this.theta.Length; i++)
            {
                this.theta[i] += alpha * (reward + gamma * newActionValue - this.oldActionValue) * gradient[i];
            }
        }

        private double GetActionValue(double[] phi)
        {
            double stateValue = 0;

            for (int i = 0; i < phi.Length; i++)
            {
                stateValue += phi[i] * theta[i];
            }

            return stateValue;
        }
    }
}
