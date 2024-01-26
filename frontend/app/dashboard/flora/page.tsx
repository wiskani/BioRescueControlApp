"use client"

import bannerFlora from "../../../public/images/banner-flora.gif"



export default function Flora() {

return (
        <div>
                <div
                        className="w-full bg-cover bg-center"
                        style={{
                        height: "28rem",
                        backgroundImage: `url(${bannerFlora.src})`,
                        }}
                        >
                        <div
                        className="flex items-center justify-center h-full w-full bg-gray-900 bg-opacity-50"
                        >
                                <div className="text-center">
                                        <h1
                                        className="text-white text-2xl font-semibold uppercase md:text-3xl"
                                        >
                                        Rescate de <span className="text-emerald-400">Flora</span>
                                        </h1>
                                </div>
                        </div>

                </div>
        </div>


)
        }
