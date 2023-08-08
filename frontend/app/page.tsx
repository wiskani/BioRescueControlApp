"use client";

import { signIn } from "next-auth/react";
import { useSession  } from 'next-auth/react'
import { useRef, useEffect } from "react";
import Image from 'next/image'
import { redirect } from 'next/navigation';

interface IProps {
  searchParams?: { [key: string]: string | string[] | undefined };
}

export default function HomePage({ searchParams }: IProps) {
    const userName = useRef("");
    const pass = useRef("");
    const { data: session } = useSession();

    const onSubmit = async () => {
      const result = await signIn("credentials", {
        username: userName.current,
        password: pass.current,
        redirect: true,
        callbackUrl: "/dashboard",
      });
    };
    if (session?.user) {
        redirect('/dashboard')
    }
    return(
      <section className='bg-gray-50 min-h-screen flex items-center justify-center'> 
          {/*login container*/}
          <div className='bg-gray-100 flex rounded-2xl shadow-lg max-w-3xl p-5 items-center'>
              {/*form*/}
              <div className="md:w-1/2 px-8 md:px-16">
                <Image src="/images/logo_blue.png" alt="logo" width={150} height={80} className='pb-4' />
                <p  className='flex items-center mb-6 text-2xl font-semibold text-emerald'>
                    Rescate de Flora y Fauna
                </p>
                <h1 className='text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl'>
                    Iniciar Sesión
                </h1>
                <form className='flex flex-col gap-4'>
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
              {/*image*/}
              <div className="md:block hidden w-1/2">
                  <Image
                     alt=" "
                     className="rounded-2xl"
                    width={150}
                      height={225}
                     src="/images/portada.png"/>
              </div>
          </div>
      </section>
    )


}
