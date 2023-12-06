const mySuper = {
    r40487: function () {
        var t = {
            utf8: {
                stringToBytes: function (e) {
                    return t.bin.stringToBytes(unescape(encodeURIComponent(e)))
                },
                bytesToString: function (e) {
                    return decodeURIComponent(escape(t.bin.bytesToString(e)))
                }
            },
            bin: {
                stringToBytes: function (e) {
                    for (var t = [], r = 0; r < e.length; r++)
                        t.push(255 & e.charCodeAt(r));
                    return t
                },
                bytesToString: function (e) {
                    for (var t = [], r = 0; r < e.length; r++)
                        t.push(String.fromCharCode(e[r]));
                    return t.join("")
                }
            }
        };
        return t;
    },
    r71012: function () {
        var t, r;
        t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
            r = {
                rotl: function (e, t) {
                    return e << t | e >>> 32 - t
                },
                rotr: function (e, t) {
                    return e << 32 - t | e >>> t
                },
                endian: function (e) {
                    if (e.constructor == Number)
                        return 16711935 & r.rotl(e, 8) | 4278255360 & r.rotl(e, 24);
                    for (var t = 0; t < e.length; t++)
                        e[t] = r.endian(e[t]);
                    return e
                },
                randomBytes: function (e) {
                    for (var t = []; e > 0; e--)
                        t.push(Math.floor(256 * Math.random()));
                    return t
                },
                bytesToWords: function (e) {
                    for (var t = [], r = 0, i = 0; r < e.length; r++,
                        i += 8)
                        t[i >>> 5] |= e[r] << 24 - i % 32;
                    return t
                },
                wordsToBytes: function (e) {
                    for (var t = [], r = 0; r < 32 * e.length; r += 8)
                        t.push(e[r >>> 5] >>> 24 - r % 32 & 255);
                    return t
                },
                bytesToHex: function (e) {
                    for (var t = [], r = 0; r < e.length; r++)
                        t.push((e[r] >>> 4).toString(16)),
                            t.push((15 & e[r]).toString(16));
                    return t.join("")
                },
                hexToBytes: function (e) {
                    for (var t = [], r = 0; r < e.length; r += 2)
                        t.push(parseInt(e.substr(r, 2), 16));
                    return t
                },
                bytesToBase64: function (e) {
                    for (var r = [], i = 0; i < e.length; i += 3)
                        for (var o = e[i] << 16 | e[i + 1] << 8 | e[i + 2], s = 0; s < 4; s++)
                            8 * i + 6 * s <= 8 * e.length ? r.push(t.charAt(o >>> 6 * (3 - s) & 63)) : r.push("=");
                    return r.join("")
                },
                base64ToBytes: function (e) {
                    e = e.replace(/[^A-Z0-9+\/]/ig, "");
                    for (var r = [], i = 0, o = 0; i < e.length; o = ++i % 4)
                        0 != o && r.push((t.indexOf(e.charAt(i - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | t.indexOf(e.charAt(i)) >>> 6 - 2 * o);
                    return r
                }
            };
        return r;
    },
    r48738: function (e) {
        function isBuffer(e) {
            return !!e.constructor && "function" == typeof e.constructor.isBuffer && e.constructor.isBuffer(e)
        }

        return null != e && (isBuffer(e) || "function" == typeof e.readFloatLE && "function" == typeof e.slice && isBuffer(e.slice(0, 0)) || !!e._isBuffer)
    },
    puper: function (e, t) {
        "use strict";
        var i, o, s, l, u;
        i = mySuper.r71012(),
            o = mySuper.r40487().utf8,
            s = mySuper.r48738(),
            l = mySuper.r40487().bin,
            (u = function (e, t) {
                    e.constructor == String ? e = t && "binary" === t.encoding ? l.stringToBytes(e) : o.stringToBytes(e) : s(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || e.constructor === Uint8Array || (e = e.toString());
                    for (var r = i.bytesToWords(e), c = 8 * e.length, d = 1732584193, f = -271733879, p = -1732584194, h = 271733878, g = 0; g < r.length; g++)
                        r[g] = (r[g] << 8 | r[g] >>> 24) & 16711935 | (r[g] << 24 | r[g] >>> 8) & 4278255360;
                    r[c >>> 5] |= 128 << c % 32,
                        r[(c + 64 >>> 9 << 4) + 14] = c;
                    for (var v = u._ff, _ = u._gg, m = u._hh, y = u._ii, g = 0; g < r.length; g += 16) {
                        var b = d
                            , R = f
                            , E = p
                            , S = h;
                        d = v(d, f, p, h, r[g + 0], 7, -680876936),
                            h = v(h, d, f, p, r[g + 1], 12, -389564586),
                            p = v(p, h, d, f, r[g + 2], 17, 606105819),
                            f = v(f, p, h, d, r[g + 3], 22, -1044525330),
                            d = v(d, f, p, h, r[g + 4], 7, -176418897),
                            h = v(h, d, f, p, r[g + 5], 12, 1200080426),
                            p = v(p, h, d, f, r[g + 6], 17, -1473231341),
                            f = v(f, p, h, d, r[g + 7], 22, -45705983),
                            d = v(d, f, p, h, r[g + 8], 7, 1770035416),
                            h = v(h, d, f, p, r[g + 9], 12, -1958414417),
                            p = v(p, h, d, f, r[g + 10], 17, -42063),
                            f = v(f, p, h, d, r[g + 11], 22, -1990404162),
                            d = v(d, f, p, h, r[g + 12], 7, 1804603682),
                            h = v(h, d, f, p, r[g + 13], 12, -40341101),
                            p = v(p, h, d, f, r[g + 14], 17, -1502002290),
                            f = v(f, p, h, d, r[g + 15], 22, 1236535329),
                            d = _(d, f, p, h, r[g + 1], 5, -165796510),
                            h = _(h, d, f, p, r[g + 6], 9, -1069501632),
                            p = _(p, h, d, f, r[g + 11], 14, 643717713),
                            f = _(f, p, h, d, r[g + 0], 20, -373897302),
                            d = _(d, f, p, h, r[g + 5], 5, -701558691),
                            h = _(h, d, f, p, r[g + 10], 9, 38016083),
                            p = _(p, h, d, f, r[g + 15], 14, -660478335),
                            f = _(f, p, h, d, r[g + 4], 20, -405537848),
                            d = _(d, f, p, h, r[g + 9], 5, 568446438),
                            h = _(h, d, f, p, r[g + 14], 9, -1019803690),
                            p = _(p, h, d, f, r[g + 3], 14, -187363961),
                            f = _(f, p, h, d, r[g + 8], 20, 1163531501),
                            d = _(d, f, p, h, r[g + 13], 5, -1444681467),
                            h = _(h, d, f, p, r[g + 2], 9, -51403784),
                            p = _(p, h, d, f, r[g + 7], 14, 1735328473),
                            f = _(f, p, h, d, r[g + 12], 20, -1926607734),
                            d = m(d, f, p, h, r[g + 5], 4, -378558),
                            h = m(h, d, f, p, r[g + 8], 11, -2022574463),
                            p = m(p, h, d, f, r[g + 11], 16, 1839030562),
                            f = m(f, p, h, d, r[g + 14], 23, -35309556),
                            d = m(d, f, p, h, r[g + 1], 4, -1530992060),
                            h = m(h, d, f, p, r[g + 4], 11, 1272893353),
                            p = m(p, h, d, f, r[g + 7], 16, -155497632),
                            f = m(f, p, h, d, r[g + 10], 23, -1094730640),
                            d = m(d, f, p, h, r[g + 13], 4, 681279174),
                            h = m(h, d, f, p, r[g + 0], 11, -358537222),
                            p = m(p, h, d, f, r[g + 3], 16, -722521979),
                            f = m(f, p, h, d, r[g + 6], 23, 76029189),
                            d = m(d, f, p, h, r[g + 9], 4, -640364487),
                            h = m(h, d, f, p, r[g + 12], 11, -421815835),
                            p = m(p, h, d, f, r[g + 15], 16, 530742520),
                            f = m(f, p, h, d, r[g + 2], 23, -995338651),
                            d = y(d, f, p, h, r[g + 0], 6, -198630844),
                            h = y(h, d, f, p, r[g + 7], 10, 1126891415),
                            p = y(p, h, d, f, r[g + 14], 15, -1416354905),
                            f = y(f, p, h, d, r[g + 5], 21, -57434055),
                            d = y(d, f, p, h, r[g + 12], 6, 1700485571),
                            h = y(h, d, f, p, r[g + 3], 10, -1894986606),
                            p = y(p, h, d, f, r[g + 10], 15, -1051523),
                            f = y(f, p, h, d, r[g + 1], 21, -2054922799),
                            d = y(d, f, p, h, r[g + 8], 6, 1873313359),
                            h = y(h, d, f, p, r[g + 15], 10, -30611744),
                            p = y(p, h, d, f, r[g + 6], 15, -1560198380),
                            f = y(f, p, h, d, r[g + 13], 21, 1309151649),
                            d = y(d, f, p, h, r[g + 4], 6, -145523070),
                            h = y(h, d, f, p, r[g + 11], 10, -1120210379),
                            p = y(p, h, d, f, r[g + 2], 15, 718787259),
                            f = y(f, p, h, d, r[g + 9], 21, -343485551),
                            d = d + b >>> 0,
                            f = f + R >>> 0,
                            p = p + E >>> 0,
                            h = h + S >>> 0
                    }
                    return i.endian([d, f, p, h])
                }
            )._ee = function (e) {
                var t = e[20]
                    , r = e.split("");
                return r[20] = r[24],
                    r[24] = t,
                    r.join("")
            }
            ,
            u._ff = function (e, t, r, i, o, s, l) {
                var u = e + (t & r | ~t & i) + (o >>> 0) + l;
                return (u << s | u >>> 32 - s) + t
            }
            ,
            u._gg = function (e, t, r, i, o, s, l) {
                var u = e + (t & i | r & ~i) + (o >>> 0) + l;
                return (u << s | u >>> 32 - s) + t
            }
            ,
            u._hh = function (e, t, r, i, o, s, l) {
                var u = e + (t ^ r ^ i) + (o >>> 0) + l;
                return (u << s | u >>> 32 - s) + t
            }
            ,
            u._ii = function (e, t, r, i, o, s, l) {
                var u = e + (r ^ (t | ~i)) + (o >>> 0) + l;
                return (u << s | u >>> 32 - s) + t
            }
            ,
            u._blocksize = 16,
            u._digestsize = 16;

        if (null == e)
            throw Error("Illegal argument " + e);

        var r = i.wordsToBytes(u(e, t));
        return t && t.asBytes ? r : t && t.asString ? l.bytesToString(r) : u._ee(i.bytesToHex(r))
    }
};
