def filter_cook(queryset,status):
    if '1' in status:
        # for i in queryset:
        context = {
            "queryset": queryset,
            "pending_cook": "checked",
            "approved_cook": ""
        }
        if '2' in status:
            context = {
                "queryset": queryset,
                "pending_cook": "checked",
                "approved_cook": "checked"
            }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "checked"
                }
                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }

                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": ""
                    }
            elif '4' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "",
                    "approved_fsc": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    print("elseeeeee")
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "",
                        "approved_fsc": "checked"
                    }
        elif '4' in status:
            context = {
                "queryset": queryset,
                "pending_cook": "checked",
                "approved_cook": "",
                "pending_fsc": "",
                "approved_fsc": "checked"
            }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "",
                    "approved_fsc": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "",
                        "approved_fsc": "checked"
                    }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "",
                    "pending_fsc": "checked",
                    "approved_fsc": "checked"
                }


            else:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "",
                    "pending_fsc": "",
                    "approved_fsc": "checked"
                }

        elif '3' in status:

            print('333333333')
            # context = {
            #     "queryset": queryset,
            #     "pending_cook": "checked",
            #     "approved_cook": "",
            #     "pending_fsc": "checked",
            #     "approved_fsc": ""
            # }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "checked",
                    "approved_fsc": ""
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": ""
                    }
            if '4' in status:
                print('444444')
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "",
                    "pending_fsc": "checked",
                    "approved_fsc": "checked"
                }
                if '2' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
            else:
                print("elseeee")
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "",
                    "pending_fsc": "checked",
                    "approved_fsc": ""
                }

    elif '2' in status:
        print("2 dfoinv")
        context = {
            "queryset": queryset,
            "pending_cook": "",
            "approved_cook": "checked"
        }
        if '3' in status:
            print("3333")
            context = {
                "queryset": queryset,
                "pending_cook": "",
                "approved_cook": "checked",
                "pending_fsc": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "checked",
                    "approved_fsc": ""
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": ""
                    }

            elif '4' in status:
                print('44444444')
                context = {
                    "queryset": queryset,
                    "pending_cook": "",
                    "approved_cook": "checked",
                    "pending_fsc": "checked",
                    "approved_fsc": "checked"
                }
                if '1' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
            else:
                context = {
                    "queryset": queryset,
                    "pending_cook": "",
                    "approved_cook": "checked",
                    "pending_fsc": "checked",
                    "approved_fsc": ""

                }

        # else:
        #     context = {
        #         "queryset": queryset,
        #         "pending_cook": "",
        #         "approved_cook": "checked",
        #         "pending_fsc": ""
        #     }
        elif '4' in status:
            print("2nd wala 444")
            context = {
                "queryset": queryset,
                "pending_cook": "",
                "approved_cook": "checked",
                "pending_fsc": "",
                "approved_fsc": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "checked",
                    "pending_fsc": "",
                    "approved_fsc": "checked"
                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
                else:
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "",
                        "approved_fsc": "checked"
                    }

            else:
                print("dhar hu mai")
                context = {
                    "queryset": queryset,
                    "pending_cook": "",
                    "approved_cook": "checked",
                    "pending_fsc": "",
                    "approved_fsc": "checked"
                }

    elif '3' in status:
        print("3 senw")
        context = {
            "queryset": queryset,
            "pending_cook": "",
            "approved_cook": "",
            "pending_fsc": "checked"
        }
        if '4' in status:
            context = {
                "queryset": queryset,
                "pending_cook": "",
                "approved_cook": "",
                "pending_fsc": "checked",
                "approved_fsc": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "pending_cook": "checked",
                    "approved_cook": "",
                    "pending_fsc": "checked",
                    "approved_fsc": "checked"
                }
                if '2' in status:
                    print("22222")
                    context = {
                        "queryset": queryset,
                        "pending_cook": "checked",
                        "approved_cook": "checked",
                        "pending_fsc": "checked",
                        "approved_fsc": "checked"
                    }
    elif '4' in status:
        print("4444")
        context = {
            "queryset": queryset,
            "pending_cook": "",
            "approved_cook": "",
            "pending_fsc": "",
            "approved_fsc": "checked"
        }
        if '1' in status:
            context = {
                "queryset": queryset,
                "pending_cook": "checked",
                "approved_cook": "",
                "pending_fsc": "",
                "approved_fsc": "checked"
            }
    elif '0' in status:
        context = {
            "queryset": queryset,
            "all": "checked",
            "pending_cook": "",
            "approved_cook": "",
            "pending_fsc": "",
            "approved_fsc": ""
        }
    else:
        context = {
            "queryset": queryset,
            "all": "",
            "pending_cook": "",
            "approved_cook": "",
            "pending_fsc": ""
        }

    return context