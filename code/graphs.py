import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

def bars(bar_data):
    df = pd.DataFrame(bar_data, columns=['Model', 'Episodes', 'Time'])

    sns.barplot(x='Model', y='Time', data=df, palette='bright')
    plt.title('Total Training Times in Mins')
    plt.savefig("graphs/bars/combined_times.png")
    plt.clf()

    sns.barplot(x='Model', y='Episodes', data=df, palette='bright')
    plt.title('Total Training Episodes')
    plt.savefig("graphs/bars/combined_total_episodes.png")
    plt.clf()

    df['Time_per_Episode'] = df['Time'] / df['Episodes']
    
    sns.barplot(x='Model', y='Time_per_Episode', data=df, palette='bright')
    plt.title('Average Time per Episode')
    plt.savefig("graphs/bars/combined_average_time_per_episode.png")
    plt.clf()

def single_graphs(models):
    for m in models:
        df = pd.read_csv(f"episodes/model_{m}_episodes.csv")
        
        sns.set(rc={'figure.figsize':(10,6)})
        sns.set_style("whitegrid")
        snsplt = sns.lineplot(data=df, x="Update",  y="Episodes")
        snsplt.set(xlabel='Updates', ylabel='Number of Episodes')
        fig = snsplt.get_figure()
        fig.suptitle("Number of Episodes per Policy Update", fontsize=12, y=0.93)
        fig.savefig(f"graphs/singles/episodes/{m}_episodes.png")
        plt.clf()

        df2 = pd.read_csv(f"metrics/model_{m}_metrics.csv")
        bar_data.append([m, df.iloc[-1, 0] + 1, (df2['Time'].sum()/60)])

        df_list = []
        df = pd.read_csv(f"logs/{m}/progress.csv")
        updates = df['time/iterations'].iloc[-1]
        df_list.append(df)
        df = pd.read_csv(f"logs/{m}_2/progress.csv")
        df['time/iterations'] = df['time/iterations'] + updates + 1
        df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)

        sns.set(rc={'figure.figsize':(10,6)})
        sns.set_style("whitegrid")
        snsplt = sns.lineplot(data=df, x="time/iterations",  y="rollout/ep_rew_mean")
        snsplt.set(xlabel='Updates', ylabel='Mean Reward')
        fig = snsplt.get_figure()
        fig.suptitle("Mean Reward of Each Policy Update", fontsize=12, y=0.93)
        fig.savefig(f"graphs/singles/mean rewards/{m}_mean_rewards.png")
        plt.clf()

        sns.set(rc={'figure.figsize':(10,6)})
        sns.set_style("whitegrid")
        snsplt = sns.lineplot(data=df, x="time/iterations",  y="rollout/ep_len_mean")
        snsplt.set(xlabel='Updates', ylabel='Mean Length')
        fig = snsplt.get_figure()
        fig.suptitle("Mean Length of Episodes in Each Policy Update", fontsize=12, y=0.93)
        fig.savefig(f"graphs/singles/episode lengths/{m}_mean_len.png")
        plt.clf()

def combined_graphs(models):
    df_list = []
    for i in models:
        df = pd.read_csv(f"episodes/model_{i}_episodes.csv")
        df['Model'] = i
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)

    sns.set(rc={'figure.figsize':(10,6)})
    sns.set_style("whitegrid")
    snsplt = sns.lineplot(data=combined_df, x="Update",  y="Episodes", hue="Model", palette="bright")
    snsplt.set(xlabel='Updates', ylabel='Number of Episodes')
    fig = snsplt.get_figure()
    fig.suptitle("Number of Episodes per Policy Update", fontsize=12, y=0.93)
    fig.savefig("graphs/combined/episodes_combined.png")
    plt.clf()

    df_list = []
    for i in models:
        list = []
        df = pd.read_csv(f"logs/{i}/progress.csv")
        updates = df['time/iterations'].iloc[-1]
        list.append(df)
        df = pd.read_csv(f"logs/{i}_2/progress.csv")
        df['time/iterations'] = df['time/iterations'] + updates + 1
        list.append(df)
        df = pd.concat(list, ignore_index=True)

        df['Model'] = i
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)

    sns.set(rc={'figure.figsize':(10,6)})
    sns.set_style("whitegrid")
    snsplt = sns.lineplot(data=combined_df, x="time/iterations",  y="rollout/ep_rew_mean", hue="Model", palette="bright")
    snsplt.set(xlabel='Updates', ylabel='Mean Reward')
    fig = snsplt.get_figure()
    fig.suptitle("Mean Reward of Each Policy Update", fontsize=12, y=0.93)
    fig.savefig("graphs/combined/mean_rewards_combined.png")
    plt.clf()

    sns.set(rc={'figure.figsize':(10,6)})
    sns.set_style("whitegrid")
    snsplt = sns.lineplot(data=combined_df, x="time/iterations",  y="rollout/ep_len_mean", hue="Model", palette="bright")
    snsplt.set(xlabel='Updates', ylabel='Mean Length')
    fig = snsplt.get_figure()
    fig.suptitle("Mean Length of Episodes in Each Policy Update", fontsize=12, y=0.93)
    fig.savefig(f"graphs/combined/mean_len_combined.png")
    plt.clf()

if __name__ == "__main__":
    # models = []
    # bar_data = []
    # file_names = os.listdir("metrics")
    # for file_name in file_names:
    #     parts = file_name.split('_')
    #     models.append(parts[1])

    # single_graphs(models)
    # bars(bar_data)

    # combined_models = []
    # #combined_graphs(combined_models)
    # combined_graphs(models)

    file_names = os.listdir('distances')
    df3 = pd.read_csv(f'distances/{file_names[0]}')
    df4 = pd.read_csv(f'distances/{file_names[1]}')
    df3['model'] = 'GA 1'
    df4['model'] = 'GA 2'
    df1 = pd.read_csv(f'distances/{file_names[2]}')
    df2 = pd.read_csv(f'distances/{file_names[3]}')
    df1['model'] = 'PPO 1'
    df2['model'] = 'PPO 2'

    combined_df = pd.concat([df1, df2, df3, df4])

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Experiment', y='Distance', hue='model', data=combined_df, ci=None, palette='Set2')
    plt.xlabel('Experiment')
    plt.ylabel('Distance Raced')
    plt.legend(title='Model')
    plt.grid(True)
    plt.savefig("algs.png")
    plt.clf()