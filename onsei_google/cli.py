# -*- coding: utf-8 -*-
"""
    onsei_google.cli
    ~~~~~~~~~~~~~~~~

    An `agent` command group for Flasks CLI interface.

    :copyright: (c) 2018 ONSEI GmbH
    :license: Proprietary
"""

import click
from flask import current_app
from flask.cli import AppGroup

from tabulate import tabulate

from onsei_google.utils import fqn


@click.group(cls=AppGroup)
def agent_cli():
    """Interact with the Dialogflow agent."""


@agent_cli.command('intents')
def intents():
    """List the registered intent handlers.

    Prints a table with the registered intent names and their handler
    functions.
    """
    with current_app.app_context():
        agent = current_app.extensions['onsei_google']
        data = list(agent.list_handler())
    data.sort(key=lambda intent_handler: intent_handler[0])
    table_data = [(intent, fqn(handler)) for intent, handler in data]
    table = tabulate(table_data, headers=('Intent', 'Handler'))
    click.echo(table)


@agent_cli.command('contexts')
def contexts():
    """List the registered contexts.

    Prints a table with the registered context names, their default factories
    and whether they should be kept around.
    """
    with current_app.app_context():
        agent = current_app.extensions['onsei_google']
        context_processors = list(agent.list_contexts())
    data = [
        (ctx.display_name, fqn(ctx.default_factory), ctx.keep_around)
        for ctx in context_processors
    ]
    headers = ('Name', 'Default', 'Keep around')
    table = tabulate(data, headers)
    click.echo(table)


@agent_cli.command('integrations')
def integrations():
    """List the registered integration conversation classes.

    Prints a table with the registered integrations (source and version), the
    corresponding conversation class and its init kwargs.
    """
    with current_app.app_context():
        agent = current_app.extensions['onsei_google']
        data = list(agent.list_integrations())
    headers = ('Integration', 'Version', 'Integration class', 'Init kwargs')
    table = tabulate(data, headers)
    click.echo(table)
