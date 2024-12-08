import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy, Policy
from student_submissions.s2210xxx.policy2310068 import Policy2310068
# from student_submissions.s2210xxx.FFD_policy import FFD

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 1

if __name__ == "__main__":
    # # Reset the environment
    # observation, info = env.reset(seed=42)
    # print("==============================Greedy=======================================")
    # # Test GreedyPolicy
    # sum = 0
    # trim = 0
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         sum += info["filled_ratio"]
    #         trim += info["trim_loss"]
    #         observation, info = env.reset(seed=ep)
    #         ep += 1
    # print("Average fill ratio: ", sum/NUM_EPISODES)
    # print("Average trim loss: ", trim/NUM_EPISODES) 
    # # Reset the environment
    # observation, info = env.reset(seed=42)
    # print("==============================Random=======================================")
    # # Test RandomPolicy
    # rd_policy = RandomPolicy()
    # sum = 0
    # trim = 0
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         sum += info["filled_ratio"]
    #         trim += info["trim_loss"]
    #         observation, info = env.reset(seed=ep)
    #         ep += 1
    # print("Average fill ratio: ", sum/NUM_EPISODES)
    # print("Average trim loss: ", trim/NUM_EPISODES) 
    # print("==============================FFD==========================================")
    observation, info = env.reset(seed=16)
    print(info)
    ep = 0
    policy2210xxx = Policy2310068(policy_id=1)
    print("Running policy: ", policy2210xxx.policy_name)
    while ep < NUM_EPISODES:
        action = policy2210xxx.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            print(info)
            observation, info = env.reset(seed=16)
            ep += 1
env.close()
