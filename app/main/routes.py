from app.main import bp

@bp.route('/')
def index():
    return 'Flask Skeleton App'