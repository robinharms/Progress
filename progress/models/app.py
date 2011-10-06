from progress.models.factories import createContent


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = bootstrap_root()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']


def bootstrap_root():
    root = createContent('SiteRoot', title='Progress')
    root['users'] = createContent('Users')
    #Create admin user with password admin as standard
    admin = createContent('User',
                          password='admin',
                          first_name='Administrator')
    root['users']['admin'] = admin
    #Add admin to group managers
    #root.add_groups('admin', [security.ROLE_ADMIN])
    
    #Create example project
    root['example-project'] = createContent('Project')

    return root
