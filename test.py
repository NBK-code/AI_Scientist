
from src.schemas import DiscoveryRecord

record = DiscoveryRecord(
    title="A Survey on Continual Learning",
    authors=["Davide Parisi", "Ronald Kemker"],
    year=2019,
    type="survey",
    source="arxiv",
    citations=None,
    url="https://arxiv.org/abs/1802.07569",
    abstract_or_snippet="This survey reviews continual learning methods..."
)

print(record)
