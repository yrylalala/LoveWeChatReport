create table message
(
    msgId             int               not null comment '消息id'
        primary key,
    msgSvrId          bigint            null,
    type              bigint            null comment '消息类型；1-文字;3-图片;34-语音',
    status            bigint            null,
    isSend            bigint            null comment '是否是发送消息 0-否;1-是',
    isShowTimer       bigint            null,
    createTime        bigint            null comment '消息时间',
    talker            text              null comment '聊天对象',
    content           text              null,
    imgPath           text              null,
    reserved          text              null comment '消息内容',
    lvbuffer          blob              null,
    transContent      text              null,
    transBrandWording text              null,
    talkerId          bigint            null,
    bizClientMsgId    text              null,
    bizChatId         bigint default -1 null,
    bizChatUserId     text              null,
    msgSeq            bigint            null,
    flag              bigint            null,
    solitaireFoldInfo blob              null,
    historyId         text              null
)
    comment '消息记录表';

create table log
(
    id       bigint auto_increment comment '消息id'
        primary key,
    user     varchar(100) null comment '发送消息者',
    datetime datetime     null comment '消息时间',
    content  text         null comment '消息内容',
    type     bigint       null comment '消息类型 1-文字;3-图片;34-语音'
)
    comment '消息导出表';``