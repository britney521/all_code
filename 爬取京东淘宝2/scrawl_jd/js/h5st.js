r({
                                        appId: Ur.fasten,
                                        debug: !1
                                    }).sign({
                                        functionId: t.functionId,
                                        appid: t.appid,
                                        client: t.client,
                                        clientVersion: t.clientVersion,
                                        t: t.t,
                                        body: t.body && Vr(t.body)
                                    });

// Vr 是sha256 加密