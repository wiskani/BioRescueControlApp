"use client";

import { signIn } from "next-auth/react";
import { useRef } from "react";
import Image from 'next/image'

interface IProps {
  searchParams?: { [key: string]: string | string[] | undefined };
}

const LoginPage = ({ searchParams }: IProps) => {
  const userName = useRef("");
  const pass = useRef("");

  const onSubmit = async () => {
    const result = await signIn("credentials", {
      username: userName.current,
      password: pass.current,
      redirect: true,
      callbackUrl: "/",
    });
  };

  return(
    <div className='bg-gray-50'> 
        <div className='flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0'>
            <Image src="/images/logo_blue.png" alt="logo" width={150} height={80} className='pb-4' />
            <p  className='flex items-center mb-6 text-2xl font-semibold text-emerald'>
                Rescate de Flora y Fauna
            </p>
            <div className='w-full bg-white rounded-lg  shadow-2xl md:mt-0 sm:max-w-md xl:p-0'>
                <div className='p-6 space-y-4 md:space-y-6 sm:p-8'>
                    <h1 className='text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl'>
                        Iniciar Sesión
                    </h1>
                    <form className='space-y-4 md:space-y-6'>
                        <div >
                            <label className='block mb-2 text-sm font-medium text-gray-900' >Correo electronico</label>
                            <input 
                                onChange={(e) => (userName.current = e.target.value)}
                                type='email'
                                className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
                            />
                        </div>
                        <div>
                            <label className='block mb-2 text-sm font-medium text-gray-900' >Contraseña</label>
                            <input 
                                onChange={(e) => (pass.current = e.target.value)}
                                type='password'
                                className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
                             />
                        </div>
                        <div className='flex items-center justify-between' >
                            <a className='text-sm font-medium text-primary-600 hover:underline'>Olvide mi contraseña</a>
                        </div>
                        <button
                            onClick={onSubmit}
                            type="button" 
                            className='w-full text-white bg-emerald-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center'
                        >
                            LOGIN
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
  )
}

export default LoginPage;
