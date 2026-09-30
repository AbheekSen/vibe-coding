"""
collision: ball-vs-brick collision handling.
"""


def handle_ball_brick_collision(ball, brick):
    """
    If the ball overlaps the brick, bounce it off and return True.

    Works for every brick type (the bounce is the same; what happens to the
    brick afterwards is decided by the caller). The bounce axis is picked
    from the smaller overlap so side hits reflect horizontally, and the ball
    is pushed out of the brick so it can never get stuck inside it.
    """
    ball_rect = ball.get_rect()
    brick_rect = brick.get_rect()
    if not ball_rect.colliderect(brick_rect):
        return False

    overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
    overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)

    if overlap_x < overlap_y:
        if ball_rect.centerx < brick_rect.centerx:
            ball.x -= overlap_x
            ball.vx = -abs(ball.vx)
        else:
            ball.x += overlap_x
            ball.vx = abs(ball.vx)
    else:
        if ball_rect.centery < brick_rect.centery:
            ball.y -= overlap_y
            ball.vy = -abs(ball.vy)
        else:
            ball.y += overlap_y
            ball.vy = abs(ball.vy)
    return True
