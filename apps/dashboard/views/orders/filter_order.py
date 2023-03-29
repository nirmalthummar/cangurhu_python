def filter_order(queryset, status):
    if '1' in status:
        # for i in queryset:
        context = {
            "queryset": queryset,
            "In": "checked",
            "En": ""
        }
        if '2' in status:
            context = {
                "queryset": queryset,
                "In": "checked",
                "En": "checked"
            }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "checked"
                }
                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }

                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",
                    }
            elif '4' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "",

                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:

                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "",

                    }
        elif '4' in status:
            context = {
                "queryset": queryset,
                "In": "checked",
                "En": "",
                "Delivered": "",

            }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "",

                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "",

                    }
            if '3' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "",
                    "Delivered": "checked",

                }


            else:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "",
                    "Delivered": "",

                }

        elif '3' in status:


            # context = {
            #     "queryset": queryset,
            #     "In": "checked",
            #     "En": "",
            #     "Delivered": "checked",
            #           # }
            if '2' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "checked",
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",
                    }
            if '4' in status:

                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "",
                    "Delivered": "checked",

                }
                if '2' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "",
                        "Delivered": "checked",

                    }
            else:

                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "",
                    "Delivered": "checked",
                }

    elif '2' in status:

        context = {
            "queryset": queryset,
            "In": "",
            "En": "checked"
        }
        if '3' in status:

            context = {
                "queryset": queryset,
                "In": "",
                "En": "checked",
                "Delivered": "checked"
            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "checked",
                }

                if '4' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",
                    }

            elif '4' in status:

                context = {
                    "queryset": queryset,
                    "In": "",
                    "En": "checked",
                    "Delivered": "checked",

                }
                if '1' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "",
                        "En": "checked",
                        "Delivered": "checked",

                    }
            else:
                context = {
                    "queryset": queryset,
                    "In": "",
                    "En": "checked",
                    "Delivered": "checked",
                }

        # else:
        #     context = {
        #         "queryset": queryset,
        #         "In": "",
        #         "En": "checked",
        #         "Delivered": ""
        #     }
        elif '4' in status:

            context = {
                "queryset": queryset,
                "In": "",
                "En": "checked",
                "Delivered": "",

            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "checked",
                    "Delivered": "",

                }
                if '3' in status:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
                else:
                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "",

                    }

            else:

                context = {
                    "queryset": queryset,
                    "In": "",
                    "En": "checked",
                    "Delivered": "",

                }

    elif '3' in status:

        context = {
            "queryset": queryset,
            "In": "",
            "En": "",
            "Delivered": "checked"
        }
        if '4' in status:
            context = {
                "queryset": queryset,
                "In": "",
                "En": "",
                "Delivered": "checked",

            }
            if '1' in status:
                context = {
                    "queryset": queryset,
                    "In": "checked",
                    "En": "",
                    "Delivered": "checked",

                }
                if '2' in status:

                    context = {
                        "queryset": queryset,
                        "In": "checked",
                        "En": "checked",
                        "Delivered": "checked",

                    }
    elif '4' in status:

        context = {
            "queryset": queryset,
            "In": "",
            "En": "",
            "Delivered": "",

        }
        if '1' in status:
            context = {
                "queryset": queryset,
                "In": "checked",
                "En": "",
                "Delivered": "",

            }
    elif '0' in status:
        context = {
            "queryset": queryset,
            "all": "checked",
            "In": "",
            "En": "",
            "Delivered": "",
        }
    else:
        context = {
            "queryset": queryset,
            "all": "",
            "In": "",
            "En": "",
            "Delivered": ""
        }

    return context