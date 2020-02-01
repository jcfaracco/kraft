# SPDX-License-Identifier: BSD-3-Clause
#
# Authors: Alexander Jung <alexander.jung@neclab.eu>
#
# Copyright (c) 2020, NEC Europe Ltd., NEC Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.

import os
import click
import subprocess
from kraft.logger import logger
from kraft.kraft import pass_environment
from kraft.app import UnikraftApp, MisconfiguredUnikraftApp

@click.command('clean', short_help='Clean the unikraft application.')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
@click.option('--proper', '-p', is_flag=True, help='Delete the build directory.')
# TODO: Distclean is useful for resetting configuration and starting fresh,
# however, we lose the .config file generated by the `kraft init` step and
# are then unable to re-trace our steps back into an original configuration.
# We need to somehow preserve tha we ued a template application or that our
# .config.orig is preserved.
# @click.option('--dist', '-d', is_flag=True, help='Delete the build directory and configuration.')
@pass_environment
def cli(ctx, path, proper):
    """
    This subcommand cleans the Unikraft application of build artifacts.
    """

    if path is None:
        path = os.getcwd()
    
    try:
        app = UnikraftApp(ctx=ctx, path=path)
    except MisconfiguredUnikraftApp as e:
        click.echo("Unsupported configuration: %s" % str(e))
        sys.exit(1)

    app.clean(proper=proper)