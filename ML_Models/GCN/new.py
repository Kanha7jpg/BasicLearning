import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GCNConv

# Reproducibility
np.random.seed(42)
torch.manual_seed(42)
np.set_printoptions(precision=6, suppress=True)


class VanillaGCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.W0 = nn.Parameter(torch.empty(input_dim, hidden_dim))
        self.W1 = nn.Parameter(torch.empty(hidden_dim, output_dim))
        nn.init.xavier_uniform_(self.W0)
        nn.init.xavier_uniform_(self.W1)

    def forward(self, X, A_hat):
        H1 = A_hat @ X @ self.W0
        H1 = torch.relu(H1)
        Z = A_hat @ H1 @ self.W1
        return H1, Z


class ThreeLayerGCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.W0 = nn.Parameter(torch.empty(input_dim, hidden_dim))
        self.W1 = nn.Parameter(torch.empty(hidden_dim, hidden_dim))
        self.W2 = nn.Parameter(torch.empty(hidden_dim, output_dim))
        nn.init.xavier_uniform_(self.W0)
        nn.init.xavier_uniform_(self.W1)
        nn.init.xavier_uniform_(self.W2)

    def propagate(self, A_hat, H, W):
        return torch.sparse.mm(A_hat, H) @ W

    def forward(self, X, A_hat):
        H1 = self.propagate(A_hat, X, self.W0)
        H1 = torch.relu(H1)
        H2 = self.propagate(A_hat, H1, self.W1)
        H2 = torch.relu(H2)
        Z = self.propagate(A_hat, H2, self.W2)
        return H1, H2, Z


class CoraGCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        return self.conv3(x, edge_index)


def build_simple_graph():
    num_nodes = 5
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]

    A = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1

    I = np.eye(num_nodes, dtype=np.float32)
    A_tilde = A + I
    degrees = A_tilde.sum(axis=1)
    D_tilde = np.diag(degrees)
    D_inv_sqrt_values = 1.0 / np.sqrt(degrees)
    D_inv_sqrt = np.diag(D_inv_sqrt_values)
    A_hat = D_inv_sqrt @ A_tilde @ D_inv_sqrt

    X = np.array([
        [1, 0],
        [0, 1],
        [1, 1],
        [0, 1],
        [1, 0],
    ], dtype=np.float32)

    y = torch.tensor([0, 0, 0, 1, 0], dtype=torch.long)
    train_mask = torch.tensor([True, False, False, True, False])
    X_tensor = torch.tensor(X, dtype=torch.float32)
    A_hat_tensor = torch.tensor(A_hat, dtype=torch.float32)

    return {
        "num_nodes": num_nodes,
        "edges": edges,
        "A": A,
        "A_tilde": A_tilde,
        "D_tilde": D_tilde,
        "D_inv_sqrt": D_inv_sqrt,
        "A_hat": A_hat,
        "X": X,
        "y": y,
        "train_mask": train_mask,
        "X_tensor": X_tensor,
        "A_hat_tensor": A_hat_tensor,
    }


def run_simple_graph_demo():
    print("\n=== Simple Graph GCN Demo ===")
    graph = build_simple_graph()
    X = graph["X"]
    y = graph["y"]
    train_mask = graph["train_mask"]
    X_tensor = graph["X_tensor"]
    A_hat_tensor = graph["A_hat_tensor"]

    model = VanillaGCN(input_dim=2, hidden_dim=2, output_dim=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    loss_history = []

    for epoch in range(500):
        model.train()
        H1, Z = model(X_tensor, A_hat_tensor)
        loss = criterion(Z[train_mask], y[train_mask])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_history.append(loss.item())

        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch + 1:3d} | Loss: {loss.item():.6f}")

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(loss_history) + 1), loss_history)
    plt.xlabel("Epoch")
    plt.ylabel("Cross-Entropy Loss")
    plt.title("Vanilla GCN Training Loss")
    plt.grid(True)
    plt.show()

    model.eval()
    with torch.no_grad():
        H1_final, Z_final = model(X_tensor, A_hat_tensor)
        probabilities = torch.softmax(Z_final, dim=1)
        predictions = torch.argmax(probabilities, dim=1)

    train_predictions = predictions[train_mask]
    train_labels = y[train_mask]
    train_accuracy = (train_predictions == train_labels).float().mean().item()
    print("Training accuracy:", train_accuracy)
    print("Final probabilities:\n", probabilities.numpy())
    print("Final predictions:\n", predictions.numpy())


def run_dense_planetoid_demo():
    print("\n=== Dense Cora GCN Demo ===")
    dataset = Planetoid(root="data/Cora", name="Cora")
    data = dataset[0]
    X = data.x.float()
    y = data.y.long()
    N = data.num_nodes

    A = torch.zeros((N, N), dtype=torch.float32)
    src = data.edge_index[0]
    dst = data.edge_index[1]
    A[src, dst] = 1.0
    A = torch.maximum(A, A.T)
    I = torch.eye(N)
    A_tilde = A + I
    degrees = A_tilde.sum(dim=1)
    D_inv_sqrt = degrees.pow(-0.5)
    edge_index = A_tilde.nonzero(as_tuple=False).T
    row = edge_index[0]
    col = edge_index[1]
    edge_weight = D_inv_sqrt[row] * D_inv_sqrt[col]
    A_hat = torch.sparse_coo_tensor(edge_index, edge_weight, size=(N, N)).coalesce()

    model = ThreeLayerGCN(
        input_dim=dataset.num_node_features,
        hidden_dim=64,
        output_dim=dataset.num_classes,
    )
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    with torch.no_grad():
        _, _, initial_Z = model(X, A_hat)
    initial_loss = criterion(initial_Z[data.train_mask], y[data.train_mask])

    for epoch in range(300):
        model.train()
        H1, H2, Z = model(X, A_hat)
        loss = criterion(Z[data.train_mask], y[data.train_mask])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 25 == 0:
            with torch.no_grad():
                train_pred = Z.argmax(dim=1)
                train_acc = (train_pred[data.train_mask] == y[data.train_mask]).float().mean()
                val_acc = (train_pred[data.val_mask] == y[data.val_mask]).float().mean()
            print(
                f"Epoch {epoch + 1:3d} | "
                f"Loss: {loss.item():.4f} | "
                f"Train Acc: {train_acc.item():.4f} | "
                f"Val Acc: {val_acc.item():.4f}"
            )

    model.eval()
    with torch.no_grad():
        H1_final, H2_final, Z_final = model(X, A_hat)
        probabilities = torch.softmax(Z_final, dim=1)
        predictions = probabilities.argmax(dim=1)
    final_loss = criterion(Z_final[data.train_mask], y[data.train_mask]).item()
    test_predictions = predictions[data.test_mask]
    test_labels = y[data.test_mask]
    test_accuracy = (test_predictions == test_labels).float().mean().item()

    print("\nFinal training loss:", final_loss)
    print("Test accuracy:", test_accuracy)


def run_cleaned_cora_demo():
    print("\n=== Cleaned Cora 3-Layer GCN Demo ===")
    dataset = Planetoid(root="data/Planetoid", name="Cora")
    data = dataset[0]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = data.to(device)

    model = CoraGCN(dataset.num_node_features, 16, dataset.num_classes).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    def train():
        model.train()
        optimizer.zero_grad()
        logits = model(data.x, data.edge_index)
        loss = F.cross_entropy(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        return loss.item()

    def classification_metrics(predictions, labels, num_classes):
        confusion = torch.zeros((num_classes, num_classes), dtype=torch.long, device=labels.device)
        indices = labels * num_classes + predictions
        confusion.view(-1).scatter_add_(0, indices, torch.ones_like(indices, dtype=torch.long))

        true_positive = confusion.diag().float()
        predicted = confusion.sum(dim=0).float()
        actual = confusion.sum(dim=1).float()
        precision_per_class = torch.nan_to_num(true_positive / predicted)
        recall_per_class = torch.nan_to_num(true_positive / actual)
        f1_per_class = torch.nan_to_num(
            2 * precision_per_class * recall_per_class / (precision_per_class + recall_per_class)
        )
        return (
            precision_per_class.mean().item(),
            recall_per_class.mean().item(),
            f1_per_class.mean().item(),
            confusion.cpu(),
        )

    @torch.no_grad()
    def test():
        model.eval()
        logits = model(data.x, data.edge_index)
        predictions = logits.argmax(dim=1)
        results = []
        for mask in (data.train_mask, data.val_mask, data.test_mask):
            labels = data.y[mask]
            masked_predictions = predictions[mask]
            accuracy = (masked_predictions == labels).float().mean().item()
            precision, recall, f1, confusion = classification_metrics(
                masked_predictions, labels, dataset.num_classes
            )
            results.append({
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "confusion": confusion,
            })
        return tuple(results)

    for epoch in range(1, 201):
        loss = train()
        if epoch == 1 or epoch % 20 == 0:
            train_metrics, val_metrics, test_metrics = test()
            print(
                f"Epoch {epoch:03d} | Loss {loss:.4f} | "
                f"Train accuracy {train_metrics['accuracy']:.4f} | "
                f"Val accuracy {val_metrics['accuracy']:.4f} | "
                f"Test accuracy {test_metrics['accuracy']:.4f}"
            )

    train_metrics, val_metrics, test_metrics = test()
    for split_name, metrics in (("Train", train_metrics), ("Validation", val_metrics), ("Test", test_metrics)):
        print(
            f"{split_name}: accuracy={metrics['accuracy']:.4f}, "
            f"precision_macro={metrics['precision']:.4f}, "
            f"recall_macro={metrics['recall']:.4f}, "
            f"f1_macro={metrics['f1']:.4f}"
        )
        print(f"{split_name} confusion matrix:\n{metrics['confusion']}")


if __name__ == "__main__":
    run_simple_graph_demo()
    run_dense_planetoid_demo()
    run_cleaned_cora_demo()
