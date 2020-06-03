try:
    from pkg_resources import get_distribution, DistributionNotFound
    __version__ = get_distribution("genesiscloud").version
except (ImportError, DistributionNotFound):
    __version__ = "0.2.0"
