
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import joblib

def preprocess_data(data):
    states = np.array([d[0] for d in data])
    actions = np.array([d[1] for d in data])
    rewards = np.array([d[2] for d in data])
    next_states = np.array([d[3] for d in data])
    done = np.array([d[4] for d in data])
    return states, actions, rewards, next_states, done


class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train_model(model, data, epochs=1000, batch_size=64, gamma=0.99):
    optimizer = optim.Adam(model.parameters())
    criterion = nn.MSELoss()
    states, actions, rewards, next_states, done = preprocess_data(data)

    for epoch in range(epochs):
        for i in range(0, len(states), batch_size):
            state_batch = torch.tensor(states[i:i+batch_size], dtype=torch.float32)
            action_batch = torch.tensor(actions[i:i+batch_size], dtype=torch.int64)
            reward_batch = torch.tensor(rewards[i:i+batch_size], dtype=torch.float32)
            next_state_batch = torch.tensor(next_states[i:i+batch_size], dtype=torch.float32)
            done_batch = torch.tensor(done[i:i+batch_size], dtype=torch.float32)

            q_values = model(state_batch)
            next_q_values = model(next_state_batch)

            # Ensure action_batch is within the valid range
            assert action_batch.max().item() < model.fc3.out_features, "Action index out of bounds"

            q_value = q_values.gather(1, action_batch.unsqueeze(1)).squeeze(1)
            next_q_value = next_q_values.max(1)[0]
            expected_q_value = reward_batch + gamma * next_q_value * (1 - done_batch)

            loss = criterion(q_value, expected_q_value.detach())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

def save_model(model, path):
    torch.save(model.state_dict(), path)

def load_model(model, path):
    model.load_state_dict(torch.load(path))
    model.eval()