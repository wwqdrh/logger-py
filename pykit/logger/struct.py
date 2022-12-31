import os
import sys

from loguru import logger as ll


def json_struct():
    ll.add(sys.stdout, serialize=True)
    ll.info("Contextualize your logger easily")
    ll.add("file.log", format="{extra[ip]} {extra[user]} {message}")
    context_logger = ll.bind(ip="192.168.0.1", user="someone")
    context_logger.info("Contextualize your logger easily")
    context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
    context_logger.info(
        "Use kwargs to add context during formatting: {user}", user="anybody"
    )
    ll.add("special.log", filter=lambda record: "special" in record["extra"])
    ll.debug("This message is not logged to the file")
    ll.bind(special=True).info("This message, though, is logged to the file!")
