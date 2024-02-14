"use client";

import React, { useState } from "react";
import { signOut, signIn, useSession } from "next-auth/react";
import { useRouter } from "next/navigation"; 
import Link from "next/link";
import Image from "next/image";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();
    const { data: session } = useSession();
    const user = session?.user;

    const handleToggle = () => {
        setIsOpen(!isOpen);
    };

    return(
        <header>
            <nav className="
                bg-emerald-900
                border-gray-200
                px-4
                lg:px-6
                py-2.5
                "
            >
                <div className="
                    flex
                    flex-wrap
                    justify-between
                    items-center
                    mx-auto
                    max-w-screen-xl
                    "
                >
                    <a href="#" className="flex items-center">
                        <Image
                            src="/images/logo_white.png"
                            className="mr-3 h-6 sm:h-9"
                            alt="Logo"
                            width={75}
                            height={40}
                        />
                    </a>
                    <button
                        className="group"
                        onClick={() => router.push("/")}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            fill="currentColor"
                            className="text-white group-hover:text-yellow-500"
                            viewBox="0 0 16 16"
                        >
                            <path
                                fillRule="evenodd"
                                d="
                                M2
                                13.5V7h1v6.5a.5.5
                                0
                                0
                                0
                                .5.5h9a.5.5
                                0 0 0
                                .5-.5V7h1v6.5a1.5
                                1.5 0 0
                                1-1.5
                                1.5h-9A1.5
                                1.5 0 0 1 2
                                13.5zm11-11V6l-2-2V2.5a.5.5
                                0 0 1
                                .5-.5h1a.5.5 0 0 1
                                .5.5z
                                "
                            />
                            <path
                                fillRule="evenodd"
                                d="
                                M7.293
                                1.5a1
                                1 0 0 1
                                1.414
                                0l6.647
                                6.646a.5.5
                                0 0
                                1-.708.708L8
                                2.207
                                1.354
                                8.854a.5.5
                                0 1
                                1-.708-.708L7.293
                                1.5z
                                "
                            />
                        </svg>
                    </button>
                    <div className="flex items-center lg:order-2">
                        <>
                            {user ? (
                                <button
                                    onClick={() => signOut()}
                                    className='
                                    w-full
                                    text-white
                                    bg-red-600
                                    hover:bg-primary-700
                                    focus:ring-4
                                    focus:outline-none
                                    focus:ring-primary-300
                                    font-medium rounded-lg
                                    text-sm
                                    px-5
                                    py-2.5
                                    text-center
                                    '
                                >
                                    Cerrar sesión
                                </button>
                            ) : (
                                    <button
                                        onClick={() => router.push("/login")}
                                        className='
                                        w-full
                                        text-gray-900
                                        bg-emerald-50
                                        hover:bg-primary-700
                                        focus:ring-4
                                        focus:outline-none
                                        focus:ring-primary-300
                                        font-medium
                                        rounded-lg
                                        text-sm
                                        px-5
                                        py-2.5
                                        text-center
                                        '
                                    >
                                        Iniciar sesión
                                    </button>
                                )}  
                        </>
                        <button
                            onClick={handleToggle}
                            data-collapse-toggle="mobile-menu-2"
                            type="button"
                            className="
                            inline-flex
                            items-center
                            p-2 ml-1
                            text-sm
                            text-gray-50
                            rounded-lg
                            lg:hidden
                            hover:bg-gray-100
                            focus:outline-none
                            focus:ring-2
                            focus:ring-gray-200
                            "
                            aria-controls="mobile-menu-2"
                            aria-expanded={false}
                        >
                            <span className="sr-only">Open main menu</span>
                            <svg
                                className="w-6 h-6"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fillRule="evenodd"
                                    d="
                                    M3
                                    5a1
                                    1 0
                                    011-1h12a1
                                    1 0
                                    110
                                    2H4a1
                                    1 0
                                    01-1-1zM3
                                    10a1 1 0
                                    011-1h12a1
                                    1 0 110
                                    2H4a1
                                    1 0
                                    01-1-1zM3
                                    15a1 1 0
                                    011-1h12a1
                                    1 0
                                    110
                                    2H4a1
                                    1 0 01-1-1z
                                    "
                                    clipRule="evenodd"
                                >
                                </path>
                            </svg>
                            <svg className="hidden w-6 h-6"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fillRule="evenodd"
                                    d="
                                    M4.293
                                    4.293a1
                                    1 0
                                    011.414
                                    0L10
                                    8.586l4.293-4.293a1
                                    1 0
                                    111.414
                                    1.414L11.414
                                    10l4.293
                                    4.293a1
                                    1 0
                                    01-1.414
                                    1.414L10
                                    11.414l-4.293
                                    4.293a1
                                    1 0
                                    01-1.414-1.414L8.586
                                    10
                                    4.293
                                    5.707a1
                                    1 0
                                    010-1.414z
                                    "
                                    clipRule="evenodd"
                                >
                                </path>
                            </svg>
                        </button>
                    </div>
                    <div
                        className={
                            `${isOpen ? '' : 'hidden'} justify-between items-center w-full lg:flex lg:w-auto lg:order-1`
                        }
                        id="mobile-menu-2"
                    >
                        <ul className="
                            flex
                            flex-col
                            mt-4
                            font-medium
                            lg:flex-row
                            lg:space-x-8
                            lg:mt-0
                            "
                        >
                            <li>
                                {
                                    user?.permissions.includes("admin")  ? (
                                        <Link
                                            href="/users"
                                            className="
                                            block
                                            py-2
                                            pr-4
                                            pl-3
                                            text-gray-50
                                            border-b
                                            border-gray-100
                                            hover:text-yellow-300
                                            hover:bg-gray-50
                                            lg:hover:bg-transparent
                                            lg:border-0
                                            lg:hover:text-primary-700
                                            lg:p-0
                                            "
                                        >
                                            Personal
                                        </Link>
                                    ) : (
                                            <>  </>
                                        )
                                }
                            </li>
                            <li>
                                <Link 
                                    href="/flora"
                                    className="
                                    block
                                    py-2
                                    pr-4
                                    pl-3
                                    text-gray-50
                                    border-b
                                    border-gray-100
                                    hover:text-yellow-300
                                    hover:bg-gray-50
                                    lg:hover:bg-transparent
                                    lg:border-0
                                    lg:hover:text-primary-700
                                    lg:p-0
                                    "
                                >
                                    Flora

                                </Link>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="
                                    block
                                    py-2
                                    pr-4
                                    pl-3
                                    text-gray-50
                                    border-b
                                    border-gray-100
                                    hover:text-yellow-300
                                    hover:bg-gray-50
                                    lg:hover:bg-transparent
                                    lg:border-0
                                    lg:hover:text-primary-700
                                    lg:p-0
                                    "
                                >
                                    Herpetofauna
                                </a>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="
                                    block
                                    py-2
                                    pr-4
                                    pl-3
                                    text-gray-50
                                    border-b
                                    border-gray-100
                                    hover:text-yellow-300
                                    hover:bg-gray-50
                                    lg:hover:bg-transparent
                                    lg:border-0
                                    lg:hover:text-primary-700
                                    lg:p-0
                                    "
                                >
                                    Mastozoología 
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Header;
