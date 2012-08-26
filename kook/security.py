from pyramid.security import Everyone, Deny, Allow

VOTE_ACTIONS = ('upvote', 'downvote')
AUTHOR_ACTIONS = ('update', 'delete', 'hide')
ADMIN_ACTIONS = ('manage_dishes', 'manage_products')

RECIPE_BASE_ACL = [
    (Allow, Everyone, 'read'),
    (Allow, 'registered', 'comment'),
    (Allow, 'upvoters', 'upvote'),
    (Allow, 'downvoters', 'downvote'),
    (Deny, 'registered', 'upvote'),
    (Deny, 'registered', 'downvote'),
    (Deny, Everyone, VOTE_ACTIONS),
    (Deny, Everyone, AUTHOR_ACTIONS)
]

COMMENT_BASE_ACL = [
    (Deny, Everyone, AUTHOR_ACTIONS)
]