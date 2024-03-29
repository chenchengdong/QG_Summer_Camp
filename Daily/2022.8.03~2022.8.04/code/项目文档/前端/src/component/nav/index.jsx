import React, { Component } from 'react'
import {Link,Outlet,useNavigate} from 'react-router-dom'
import './index.css'
import userIcon from './images/CATIA.jpg'
import searchIcon from './images/搜索.png'

export default function Nav() {

    const navigate=useNavigate();
    function toSearch(){
        console.log(searchRef.current.value);
        navigate('/search',{
            state:{
                content:searchRef.current.value
            }
        })
    }

    // search实时接受搜索框内容
    const searchRef=React.useRef();

    return (
        <div className="nav-container">
            <div className="nav">
                <ul className="nav-screen">
                    <li key='001'><Link to='/home' >首页</Link></li>
                    <li key='002'><Link to='/ranking' >排行榜</Link></li>
                    <li key='003'><Link to='/sort' >分类</Link></li>
                </ul>
                <div className="nav-right">
                    <div className="nav-search">
                        <button><div onClick={toSearch}><img src={searchIcon} alt="搜索" width='16px'/></div></button>
                        <input type="text" placeholder='搜索' ref={searchRef}/>
                    </div>
                    {/* 点击用户头像的地方的时候 要验证是否登录 已登录切换到用户个人信息页面
                    若尚未登录 则弹出登录界面 */}
                    <Link to='/login' className="nav-user-icon">
                        <img src={userIcon} alt="用户头像" width='40px'/>
                    </Link>
                </div>
            </div>
            <Outlet/>
        </div>
    )
}
