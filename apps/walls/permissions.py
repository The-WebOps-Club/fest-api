from django.db.models import Q
from misc.constants import POST_TYPE
import operator

"""
    class PermissionStack

    Coordinates a bunch of query builder functions and is ideal for
    complex permission models.

    Use a flag( a unique number ) to identify different types of posts.

    Methods:
        For initializing.
        addSubQueryBuilder( function, index )

        For running.
        getFilteredQuery( accessor, accessee )

    Class Properties:
        sub_queries :   holds the list of subquery-flaglist tuples. 
                        each entry looks like this [ sub_query, [FLAG_1, FLAG_2, ... ] ]

        flag_parameter: the name of the SQL parameter or attribute that is being
                        used for storing the flag(identifier). By default 'access_specifier'.


"""
class PermissionStack( object ):

    sub_queries = [];
    flag_parameter = 'access_specifier'

    """
        Adds a subquery builder function
        Arguments:
            func: the function to add.
            flaglist: the flags to affect.

        Returns:
            None always
    """
    def add_subquery_builder( self, func, flaglist ):
        self.sub_queries.append( [ flaglist, func ] )

    """
        Returns the full query by appending all the subqueries 
        returned by each of the builder functions.

        Arguments:
            accessor:   the accessor object( mostly User )
            accessee:   the destination object type( mostly Post )

        Returns:
            the full query. a django Q object.
    """
    def get_filtered_query( self, accessor, accessee ):
        queries = []
        for flaglist,sub_query in self.sub_queries:
            flag_filters = [ Q( ( self.flag_parameter, x ) ) for x in flaglist ]
            full_flag_filter = reduce( operator.or_, flag_filters )

            query,status = sub_query( accessor, accessee )
            print status
            print 'for'
            print flaglist
            if status == 'CONDITIONAL':
                # use the query object as there seem to be conditions attached to it.
                queries.append( query & full_flag_filter )
            elif status == 'ALLOW_ALL':
                # don't use query allow all objects within scope.
                queries.append( full_flag_filter )
            elif status == 'BLOCK_ALL':
                # don't do anything.
                pass

        return reduce( operator.or_, queries )
    

"""

    PostPermissionSubqueries

    A namespace of static functions designed
    to form the permission subqueries for 
    deciding the access level of a user 
    w.r.t a post.

"""
class PostPermissionSubqueries( object ):
    @staticmethod
    def check_public_access( user, post ):
        if( user.is_authenticated() ):
            return ( Q(), 'ALLOW_ALL' )
        else:
            return ( Q(), 'BLOCK_ALL' )

    """
        Checks if the person is part of the wall.
    """
    @staticmethod
    def check_wall_access( user, post ):
        erp_profile = user.erp_profile
        erp_coords = erp_profile.coord_relations.all()
        erp_supercoords = erp_profile.supercoord_relations.all()
        erp_cores = erp_profile.core_relations.all()
        erp_pages = erp_profile.page_relations.all()

        my_query = ( \
                Q(wall__person=erp_profile) | \
                Q(wall__subdept__in=erp_coords) | \
                Q(wall__dept__in=erp_supercoords) | \
                Q(wall__dept__in=erp_cores) | \
                Q(wall__page__in=erp_pages) | \
                Q(wall__subdept__dept__in=erp_supercoords) | \
                Q(wall__subdept__dept__in=erp_cores) | \
                Q(wall__dept__subdepts__in=erp_coords) \
                )

        return ( my_query, 'CONDITIONAL' )

    """
        Checks if the person is part of the access group of a post or it's wall
    """
    @staticmethod
    def check_wall_and_tag_access( user, post ):
        erp_profile = user.erp_profile
        erp_coords = erp_profile.coord_relations.all()
        erp_supercoords = erp_profile.supercoord_relations.all()
        erp_cores = erp_profile.core_relations.all()
        erp_pages = erp_profile.page_relations.all()
        my_query = ( \
                Q(access_users__id__exact=user.id) | \
                Q(access_subdepts__in=erp_coords) | \
                Q(access_depts__in=erp_supercoords) | \
                Q(access_depts__in=erp_cores) | \
                Q(access_pages__in=erp_pages) | \
                Q(wall__access_users__id__exact=user.id) | \
                Q(wall__access_subdepts__in=erp_coords) | \
                Q(wall__access_depts__in=erp_supercoords) | \
                Q(wall__access_depts__in=erp_cores) | \
                Q(wall__access_pages__in=erp_pages) | \
                Q(wall__person=erp_profile) | \
                Q(wall__subdept__in=erp_coords) | \
                Q(wall__dept__in=erp_supercoords) | \
                Q(wall__dept__in=erp_cores) | \
                Q(wall__page__in=erp_pages) | \
                Q(wall__subdept__dept__in=erp_supercoords) | \
                Q(wall__subdept__dept__in=erp_cores) | \
                Q(wall__dept__subdepts__in=erp_coords) \
                )

        return (my_query,'CONDITIONAL')

    """
        Let the creator of posts see his/her
        own posts. Call this and set all flags.
    """
    @staticmethod
    def check_creator_access( user, post ):
        return ( Q( by__id = user.id ),'CONDITIONAL' )

    """
        If staff or superuser, request PermissionStack to allow user
        to see all the objects with the associated flags.
    """
    @staticmethod
    def check_staff_access( user, post ):
        if( user.is_staff ):
            return ( Q(), 'ALLOW_ALL' )
        else:
            return ( Q(), 'BLOCK_ALL' )

    @staticmethod
    def check_superuser_access( user, post ):
        if( user.is_superuser ):
            return ( Q(), 'ALLOW_ALL' )
        else:
            return ( Q(), 'BLOCK_ALL' )

    @staticmethod
    def build_post_permissions_stack():
        stack = PermissionStack()
        stack.add_subquery_builder( PostPermissionSubqueries.check_public_access,[ POST_TYPE['PUBLIC'] ])
        stack.add_subquery_builder( PostPermissionSubqueries.check_wall_and_tag_access,[ POST_TYPE['PUBLIC'], POST_TYPE['PRIVATE_AND_TAGGED'] ])
        stack.add_subquery_builder( PostPermissionSubqueries.check_wall_access,[ POST_TYPE['PUBLIC'], POST_TYPE['PRIVATE_AND_TAGGED'], POST_TYPE['PRIVATE'] ])
        stack.add_subquery_builder( PostPermissionSubqueries.check_creator_access,[ POST_TYPE['PUBLIC'], POST_TYPE['PRIVATE_AND_TAGGED'], POST_TYPE['PRIVATE'], POST_TYPE['TAGGED'] ])
        stack.add_subquery_builder( PostPermissionSubqueries.check_superuser_access, [ POST_TYPE['PUBLIC'], POST_TYPE['PRIVATE_AND_TAGGED'], POST_TYPE['PRIVATE'], POST_TYPE['TAGGED'] ])
        return stack


DEFAULT_POST_PERMISSION_STACK = PostPermissionSubqueries.build_post_permissions_stack()