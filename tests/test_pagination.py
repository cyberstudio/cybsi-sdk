import json
import unittest
from io import BytesIO
from itertools import chain

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict

from cybsi.api.pagination import Page, chain_pages


class PaginationTest(unittest.TestCase):
    @staticmethod
    def _make_response(status_code=200, headers=None, data=None) -> requests.Response:
        """Make test response"""
        data = json.dumps(data).encode() if data else "[]".encode()
        response = Response()
        response.status_code = status_code
        response.headers = CaseInsensitiveDict(headers)
        response.raw = BytesIO(data)
        return response

    def test_pagination_no_next_link(self):
        response = self._make_response(200)

        page = Page(lambda: Response(), response, lambda x: x)
        self.assertIs(page.next_page(), None)

    def test_pagination_iterate_pages(self):
        expected = ["http://link1.com", "http://link2.com"]

        def pages():
            for link in expected + [""]:
                if link:
                    link_hdr = f'<l1>; rel="first",<{link}>; rel="next"'
                else:
                    link_hdr = '<l1>; rel="first"'
                yield self._make_response(200, headers={"link": link_hdr})

        actual = []
        page_gen = pages()

        page = Page(lambda _: next(page_gen), next(page_gen), lambda x: x)
        for _ in range(len(expected) + 1):
            actual.append(page.next_link)
            page = page.next_page()

        self.assertEqual(expected, actual[:2])
        self.assertIs(actual[-1], None)

    def test_pagination_get_page_data(self):
        expected = [1, 2, 3, 4]
        response = self._make_response(200, data=[str(i) for i in expected])

        page = Page(lambda: Response(), response, lambda x: int(x))
        self.assertEqual(expected, page.data())

    def test_pagination_iterate_page_data(self):
        expected = [1, 2, 3, 4]
        response = self._make_response(200, data=[str(i) for i in expected])

        page = Page(lambda: Response(), response, lambda x: int(x))
        actual = []
        for item in page:
            actual.append(item)

        self.assertEqual(expected, page.data())

    def test_pagination_chain_pages(self):
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        def pages():
            for page_data in data + [[]]:
                if page_data:
                    hdr = '<l1>; rel="first",<link>; rel="next"'
                else:
                    hdr = '<l1>; rel="first"'
                yield self._make_response(200, headers={"link": hdr}, data=page_data)

        actual = []
        page_gen = pages()

        page = Page(lambda _: next(page_gen), next(page_gen), lambda x: x)

        for elem, _ in zip(chain_pages(page), range(10)):
            actual.append(elem)

        expected = list(chain(*data))
        self.assertEqual(expected, actual)
