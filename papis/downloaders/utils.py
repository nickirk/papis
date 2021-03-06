import logging

import tempfile
import papis.bibtex
import papis.downloaders.aps
import papis.downloaders.arxiv
import papis.downloaders.scitationaip
import papis.downloaders.libgen
import papis.downloaders.get

logger = logging.getLogger("downloader")


def getAvailableDownloaders():
    return [
        papis.downloaders.aps.Downloader,
        papis.downloaders.arxiv.Downloader,
        papis.downloaders.scitationaip.Downloader,
        papis.downloaders.libgen.Downloader,
        papis.downloaders.get.Downloader,
    ]


def getDownloader(url):
    for downloader in getAvailableDownloaders():
        result = downloader.match(url)
        if result:
            return result
    return False


def get(url, data_format="bibtex"):
    data = dict()
    documents_paths = []
    logger.debug("Attempting to retrieve from url")
    downloader = getDownloader(url)
    if not downloader:
        logger.warning("Using downloader %s" % downloader)
        return None
    logger.debug("Using downloader %s" % downloader)
    if data_format == "bibtex":
        bibtex_data = downloader.getBibtexData()
        if bibtex_data:
            data = papis.bibtex.bibtex_to_dict(
                downloader.getBibtexData()
            )
    doc_data = downloader.getDocumentData()
    if doc_data:
        documents_paths.append(tempfile.mktemp())
        logger.debug("Saving in %s" % documents_paths[-1])
        tempfd = open(documents_paths[-1], "wb+")
        tempfd.write(doc_data)
        tempfd.close()
    return {"data": data, "documents_paths": documents_paths}
