from caral import util



describe "browsing the PyPi index skips some files":

    before each:
        self.browse = util.BrowsePyPi('', '')


    it "should skip htm files":
        pkg = "foobar.htm"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip html files":
        pkg = "foobar.html"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip org files":
        pkg = "foobar.org"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip net files":
        pkg = "foobar.net"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip http files":
        pkg = "http://foobar.me"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should not skip files with http that are non urls":
        pkg = "httplib"

        assert self.browse.should_skip_pkg(pkg) is False

    it "should not skip files with https that are non urls":
        pkg = "httpslib"

        assert self.browse.should_skip_pkg(pkg) is False
