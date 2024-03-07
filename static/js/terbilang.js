(function (f) {
    if (typeof exports === "object" && typeof module !== "undefined") {
        module.exports = f()
    } else if (typeof define === "function" && define.amd) {
        define([], f)
    } else {
        var g;
        if (typeof window !== "undefined") {
            g = window
        } else if (typeof global !== "undefined") {
            g = global
        } else if (typeof self !== "undefined") {
            g = self
        } else {
            g = this
        }
        g.angkaTerbilang = f()
    }
})(function () {
    var define, module, exports;
    return (function () {
        function r(e, n, t) {
            function o(i, f) {
                if (!n[i]) {
                    if (!e[i]) {
                        var c = "function" == typeof require && require;
                        if (!f && c) return c(i, !0);
                        if (u) return u(i, !0);
                        var a = new Error("Cannot find module '" + i + "'");
                        throw a.code = "MODULE_NOT_FOUND", a
                    }
                    var p = n[i] = {
                        exports: {}
                    };
                    e[i][0].call(p.exports, function (r) {
                        var n = e[i][1][r];
                        return o(n || r)
                    }, p, p.exports, r, e, n, t)
                }
                return n[i].exports
            }
            for (var u = "function" == typeof require && require, i = 0; i < t.length; i++) o(t[i]);
            return o
        }
        return r
    })()({
        1: [function (require, module, exports) {
            "use strict";
            var convertToUnit = function (n) {
                    return n >= 63 ? "vigintiliun" : n >= 60 ? "novemdesiliun" : n >= 57 ? "octodesiliun" : n >= 54 ? "septendesiliun" : n >= 51 ? "sexdesiliun" : n >= 48 ? "quindesiliun" : n >= 45 ? "quattuordesiliun" : n >= 42 ? "tredesiliun" : n >= 39 ? "duodesiliun" : n >= 36 ? "undesiliun" : n >= 33 ? "desiliun" : n >= 30 ? "noniliun" : n >= 27 ? "octiliun" : n >= 24 ? "septiliun" : n >= 21 ? "sextiliun" : n >= 18 ? "quintiliun" : n >= 15 ? "quadriliun" : n >= 12 ? "triliun" : n >= 9 ? "milyar" : n >= 6 ? "juta" : n >= 3 ? "ribu" : ""
                },
                numbers = ["satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan"],
                numberToString = function (n) {
                    return numbers[n - 1] || ""
                };
            module.exports = function (n) {
                for (var i = "", u = !0, e = !1, t = 0; t < n.length; t++) {
                    var r = n.length - 1 - t;
                    if (r % 3 == 0) {
                        var l = 1 != n[t] || !e && ("ribu" != convertToUnit(r) || null != n[t - 2] && 0 != n[t - 2] || null != n[t - 1] && 0 != n[t - 1]) ? "".concat(numberToString(n[t]), " ") : "se";
                        i += " ".concat(l), (n[t - 2] && 0 != n[t - 2] || n[t - 1] && 0 != n[t - 1] || 0 != n[t]) && (u = !0), u && (u = !1, i += (e ? "belas " : "") + convertToUnit(r), e && (e = !1))
                    } else r % 3 == 2 && 0 != n[t] ? i += " ".concat(1 == n[t] ? "se" : numberToString(n[t]) + " ", "ratus") : r % 3 == 1 && 0 != n[t] && (1 == n[t] ? 0 == n[t + 1] ? i += " sepuluh" : e = !0 : i += " ".concat(numberToString(n[t]), " puluh"))
                }
                return i.trim().replace(/\s+/g, " ")
            };

        }, {}]
    }, {}, [1])(1)
});