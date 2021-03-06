from threading import Thread
import unittest

try:
    from tornado.ioloop import IOLoop
except ImportError:
    raise unittest.SkipTest("Tornado not installed")

try:
    from selenium import webdriver
except ImportError:
    raise unittest.SkipTest("selenium not installed")

# Local imports.
from jigna.utils.web import get_free_port
from test_jigna_web import TestJignaWebSync, Person, patch_sys_modules
from test_jigna_vue_qt import body_vue_html


class TestJignaVueWebSync(TestJignaWebSync):
    @classmethod
    def setUpClass(cls, async=False):
        cls._backup_modules = patch_sys_modules()
        from jigna.vue_template import VueTemplate
        from jigna.web_app import WebApp
        ioloop = IOLoop.instance()
        fred = Person(name='Fred', age=42)
        template = VueTemplate(body_html=body_vue_html, async=async)
        port = get_free_port()
        app = WebApp(template=template, context={'model':fred})
        app.listen(port)

        # Start the tornado server in a different thread so that we can write
        # test statements here in the main loop
        t = Thread(target=ioloop.start)
        t.setDaemon(True)
        t.start()

        browser = webdriver.Firefox()
        browser.get('http://localhost:%d'%port)
        cls.app = app
        cls.fred = fred
        cls.browser = browser


del TestJignaWebSync


if __name__ == "__main__":
    unittest.main()
