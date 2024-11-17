import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
import torch.nn as nn
import torch.optim as optim
import sys
import os


# 定义一个简单的模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(10, 20)
        self.fc2 = nn.Linear(20, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 定义一个简单的数据集
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

# 初始化分布式环境
def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

# 清理分布式环境
def cleanup():
    dist.destroy_process_group()



# 定义模型、数据集等...

def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size, gpu_ids):
    setup(rank, world_size)
    
    # 设置使用的GPU
    print(f'这里, gpu_ids is {gpu_ids}; rank is {rank}')
    torch.cuda.set_device(gpu_ids[rank])
    device = torch.device(f"cuda:{gpu_ids[rank]}")
    
    model = MyModel().to(device)
    ddp_model = DDP(model, device_ids=[gpu_ids[rank]])
    
    dataset = MyDataset(data=torch.randn(1000, 10))
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    data_loader = DataLoader(dataset, batch_size=10, sampler=sampler)
    
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)
    
    for epoch in range(100):
        sampler.set_epoch(epoch)
        ddp_model.train()
        for data in data_loader:
            data = data.to(device)
            optimizer.zero_grad()
            output = ddp_model(data)
            loss = nn.MSELoss()(output, torch.randn(10, 10).to(device))
            loss.backward()
            print(f'loss:{loss.item()}')
            optimizer.step()
    if rank == 0:
        torch.save({
            'epoch' : epoch,
            'model_state_dict' : ddp_model.module.state_dict(),
            'optimizer_state_dict' : optimizer.state_dict()
        },'/home/wangbo/pre/result.pth')
    cleanup()

if __name__ == "__main__":
    world_size = 2
    print(sys.argv)
    rank = int(sys.argv[1][-1])
    gpu_ids = list(map(int, sys.argv[2:]))  # 从命令行参数获取GPU编号
    print(f'gpu_ids is {gpu_ids}')
    print(f'rank is {rank}')
    train(rank, world_size, gpu_ids)
    # python -m torch.distributed.launch --nproc_per_node=2 --nnodes=1 --node_rank=0 --master_addr="localhost" --master_port=12355 train.py 0 2