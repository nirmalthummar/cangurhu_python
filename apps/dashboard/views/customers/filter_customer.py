def filter_customer(queryset,status):
    if '1' in status:
        # for i in queryset:
        context = {
            "queryset": queryset,
            "blocked": "checked",
            "active": ""
        }
        if '2' in status:
            context = {
                "queryset": queryset,
                "blocked": "checked",
                "active": "checked"
            }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "checked"
                }
                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }

                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": ""
                    }
            elif '4' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "",
                    "guest": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    print("elseeeeee")
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "",
                        "guest": "checked"
                    }
        elif '4' in status:
            context = {
                "queryset": queryset,
                "blocked": "checked",
                "active": "",
                "registered": "",
                "guest": "checked"
            }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "",
                    "guest": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "",
                        "guest": "checked"
                    }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "",
                    "registered": "checked",
                    "guest": "checked"
                }


            else:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "",
                    "registered": "",
                    "guest": "checked"
                }

        elif '3' in status:

            print('333333333')
            # context = {
            #     "queryset": queryset,
            #     "blocked": "checked",
            #     "active": "",
            #     "registered": "checked",
            #     "guest": ""
            # }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "checked",
                    "guest": ""
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": ""
                    }
            if '4' in status:
                print('444444')
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "",
                    "registered": "checked",
                    "guest": "checked"
                }
                if '2' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "",
                        "registered": "checked",
                        "guest": "checked"
                    }
            else:
                print("elseeee")
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "",
                    "registered": "checked",
                    "guest": ""
                }

    elif '2' in status:
        print("2 dfoinv")
        context = {
            "queryset": queryset,
            "blocked": "",
            "active": "checked"
        }
        if '3' in status:
            print("3333")
            context = {
                "queryset": queryset,
                "blocked": "",
                "active": "checked",
                "registered": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "checked",
                    "guest": ""
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": ""
                    }

            elif '4' in status:
                print('44444444')
                context = {
                    "queryset": queryset,
                    "blocked": "",
                    "active": "checked",
                    "registered": "checked",
                    "guest": "checked"
                }
                if '1' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
            else:
                context = {
                    "queryset": queryset,
                    "blocked": "",
                    "active": "checked",
                    "registered": "checked",
                    "guest": ""

                }

        # else:
        #     context = {
        #         "queryset": queryset,
        #         "blocked": "",
        #         "active": "checked",
        #         "registered": ""
        #     }
        elif '4' in status:
            print("2nd wala 444")
            context = {
                "queryset": queryset,
                "blocked": "",
                "active": "checked",
                "registered": "",
                "guest": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "checked",
                    "registered": "",
                    "guest": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "",
                        "guest": "checked"
                    }

            else:
                print("dhar hu mai")
                context = {
                    "queryset": queryset,
                    "blocked": "",
                    "active": "checked",
                    "registered": "",
                    "guest": "checked"
                }

    elif '3' in status:
        print("3 senw")
        context = {
            "queryset": queryset,
            "blocked": "",
            "active": "",
            "registered": "checked"
        }
        if '4' in status:
            context = {
                "queryset": queryset,
                "blocked": "",
                "active": "",
                "registered": "checked",
                "guest": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "blocked": "checked",
                    "active": "",
                    "registered": "checked",
                    "guest": "checked"
                }
                if '2' in status:
                    print("22222")
                    context = {
                        "queryset": queryset,
                        "blocked": "checked",
                        "active": "checked",
                        "registered": "checked",
                        "guest": "checked"
                    }
    elif '4' in status:
        print("4444")
        context = {
            "queryset": queryset,
            "blocked": "",
            "active": "",
            "registered": "",
            "guest": "checked"
        }
        if '1' in status:
            context = {
                "queryset": queryset,
                "blocked": "checked",
                "active": "",
                "registered": "",
                "guest": "checked"
            }
    elif '0' in status:
        context = {
            "queryset": queryset,
            "all": "checked",
            "blocked": "",
            "active": "",
            "registered": "",
            "guest": ""
        }
    else:
        context = {
            "queryset": queryset,
            "all": "",
            "blocked": "",
            "active": "",
            "registered": ""
        }

    return context