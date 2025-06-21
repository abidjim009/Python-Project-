import torch
import torch.nn as nn
import math

class TransformerBlock(nn.Module):
    def __init__(self, embed_size, num_heads, ff_hidden):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_size, num_heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.ff = nn.Sequential(
            nn.Linear(embed_size, ff_hidden),
            nn.ReLU(),
            nn.Linear(ff_hidden, embed_size)
        )
        self.norm2 = nn.LayerNorm(embed_size)

    def forward(self, x):
        attn_output, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_output)
        ff_output = self.ff(x)
        return self.norm2(x + ff_output)

class TinyGPT(nn.Module):
    def __init__(self, vocab_size, embed_size=64, num_layers=2, num_heads=4, ff_hidden=256, max_len=128):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, embed_size)
        self.pos_embed = nn.Embedding(max_len, embed_size)
        self.layers = nn.ModuleList([TransformerBlock(embed_size, num_heads, ff_hidden) for _ in range(num_layers)])
        self.fc = nn.Linear(embed_size, vocab_size)

    def forward(self, x):
        seq_len = x.size(0)
        positions = torch.arange(seq_len, device=x.device).unsqueeze(1)
        x = self.token_embed(x) + self.pos_embed(positions)
        for layer in self.layers:
            x = layer(x)
        return self.fc(x)

# Example usage:
vocab_size = 1000
model = TinyGPT(vocab_size)
sample_input = torch.randint(0, vocab_size, (10, 1))  # sequence length 10
output = model(sample_input)
print(output.shape)  # [10, 1, vocab_size]
