import papis
import os
import sys
import papis.utils


class Open(papis.commands.Command):
    def init(self):

        self.parser = self.get_subparsers().add_parser(
            "open",
            help="Open document document from a given library"
        )

        self.parser.add_argument(
            "document",
            help="Document search",
            nargs="?",
            default=".",
            action="store"
        )

        self.parser.add_argument(
            "--tool",
            help="Tool for opening the file (opentool)",
            default="",
            action="store"
        )

        self.parser.add_argument(
            "-d",
            "--dir",
            help="Open directory",
            action="store_true"
        )

    def main(self):

        documentsDir = os.path.expanduser(self.config[self.args.lib]["dir"])
        if self.args.tool:
            self.config["settings"]["opentool"] = self.args.tool
        self.logger.debug("Using directory %s" % documentsDir)
        documentSearch = self.args.document
        documents = papis.utils.get_documents_in_dir(
            documentsDir,
            documentSearch
        )
        if not documents:
            print("No documents found with that name.")
            sys.exit(1)
        document = self.pick(documents)
        if not document:
            sys.exit(0)
        if not self.args.dir:
            files = document.get_files()
            file_to_open = papis.utils.pick(
                files,
                self.config,
                pick_config=dict(
                    header_filter=lambda x: x.replace(
                        document.get_main_folder(), ""
                    )
                )
            )
            papis.utils.open_file(file_to_open)
        else:
            papis.utils.open_dir(document.get_main_folder())
