import '../globals.css'
import { ReactNode } from 'react'
import Header from '../components/Header/Header'

interface IProps {
  children: ReactNode;
}

export default function Layout({
  children,
}: IProps) {
  return (
      <>
          <Header />
           {children}
      </>
  )
}
