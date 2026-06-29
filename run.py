#!/usr/bin/env python
"""Entry point for CyberTrap-AI application."""

import os
import sys
from app import create_app, db
from app.models import User, Role, Permission, Activity, Audit, Notification, Session, Backup, APIKey

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Register models in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'Activity': Activity,
        'Audit': Audit,
        'Notification': Notification,
        'Session': Session,
        'Backup': Backup,
        'APIKey': APIKey,
    }


@app.cli.command()
def init_db():
    """Initialize database."""
    db.create_all()
    print('✅ Database initialized!')


@app.cli.command()
def seed_db():
    """Seed database with initial data."""
    # Create roles
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)

    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', description='Regular User')
        db.session.add(user_role)

    viewer_role = Role.query.filter_by(name='viewer').first()
    if not viewer_role:
        viewer_role = Role(name='viewer', description='Viewer Only')
        db.session.add(viewer_role)

    db.session.commit()

    # Create admin user
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@cybertrape.local',
            is_active=True,
            is_admin=True
        )
        admin_user.set_password('Admin@123456')
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()
        print('✅ Admin user created (admin / Admin@123456)')
    else:
        print('⚠️  Admin user already exists')


@app.cli.command()
def create_admin():
    """Create new admin user."""
    import click
    username = click.prompt('Username')
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)

    if User.query.filter_by(username=username).first():
        print('❌ User already exists')
        return

    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
        db.session.commit()

    admin_user = User(username=username, email=email, is_active=True, is_admin=True)
    admin_user.set_password(password)
    admin_user.roles.append(admin_role)
    db.session.add(admin_user)
    db.session.commit()
    print(f'✅ Admin user "{username}" created successfully!')


if __name__ == '__main__':
    app.run(debug=True)
