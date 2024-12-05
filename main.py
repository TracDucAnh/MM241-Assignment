import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy, Policy
from student_submissions.s2210xxx.policy2310068 import Policy2310068

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 10

if __name__ == "__main__":
    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test GreedyPolicy
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         observation, info = env.reset(seed=ep)
    #         print(info)
    #         ep += 1

    # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test RandomPolicy
    # rd_policy = RandomPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         observation, info = env.reset(seed=ep)
    #         print(info)
    #         ep += 1

    # Uncomment the following code to test your policy
    # Reset the environment

    observation, info = env.reset(seed=42)
    print(info)

    

    policy2210xxx = Policy2310068()
    ep = 0
    sum = 0
    while (ep < NUM_EPISODES):
        action = policy2210xxx.get_action(observation, info)
        # print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            print("Episode: ", ep)
            sum += info["filled_ratio"]
            print(info)
            observation, info = env.reset()
            ep+=1
    print("Average ratio: ", sum/NUM_EPISODES)
env.close()
