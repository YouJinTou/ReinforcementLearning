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

        public int GetAction(int heroPos, double[] phi, bool isLookAhead = false)
        {
            //double epsilon = 0.1;
            //Random rand = new Random();

            //if (rand.NextDouble() < epsilon)
            //{
            //    return rand.Next(0, 3);
            //}

            int left = (heroPos - 1) >= 0 ? heroPos - 1 : heroPos;
            int doNothing = heroPos;
            int right = (heroPos + 1) < fieldWidth ? heroPos + 1 : heroPos;
            this.oldActionValue = isLookAhead ? this.oldActionValue : this.GetActionValue(phi);
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

        public double[] GetNextStateFeatures(int heroPos)
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

                    double feature = ((double)(rock.y - 18) / (rock.x * heroPos));
                    features[rock.y * 28 + rock.x] = feature;
                }
            }

            return features;
        }

        public void UpdateWeights(int reward, double[] newPhi, double[] gradient)
        {
            bool isTerminal = (reward == 0);
            double error = isTerminal ? 
                (reward - this.oldActionValue) : 
                (reward + gamma * this.GetActionValue(newPhi) - this.oldActionValue);

            for (int i = 0; i < this.theta.Length; i++)
            {
                this.theta[i] += alpha * error * gradient[i];
            }
        }

        private double GetActionValue(double[] phi)
        {
            double actionValue = 0;

            for (int i = 0; i < phi.Length; i++)
            {
                actionValue += phi[i] * theta[i];
            }

            return actionValue;
        }
    }
}