def check_alembic_postgresql_enum():
    try:
        import alembic_postgresql_enum
    except ImportError:
        raise ImportError("Please install 'alembic_postgresql_enum'")
