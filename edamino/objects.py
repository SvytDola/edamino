from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
from pydantic import BaseModel, Field


class UserProfileExtensions(BaseModel):
    privilegeOfCommentOnUserProfile: Optional[int]
    customTitles: Optional[Tuple]


class AvatarFrame(BaseModel):
    status: Optional[int]
    ownershipStatus: Any
    version: Optional[int]
    resourceUrl: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    frameType: Optional[int]
    frameId: Optional[str]


class Author(BaseModel):
    status: Optional[int]
    isNicknameVerified: Optional[bool]
    uid: Optional[str]
    level: Optional[int]
    followingStatus: Optional[int]
    accountMembershipStatus: Optional[int]
    isGlobal: Optional[bool]
    membershipStatus: Optional[int]
    reputation: Optional[int]
    role: Optional[int]
    ndcId: Optional[int]
    membersCount: Optional[int]
    nickname: Optional[str]
    icon: Optional[str]
    avatarFrame: Optional[AvatarFrame]


class UserProfile(BaseModel):
    status: Optional[int]
    moodSticker: Any
    itemsCount: Optional[int]
    consecutiveCheckInDays: Any
    uid: Optional[str]
    modifiedTime: Optional[str]
    followingStatus: Optional[int]
    onlineStatus: Optional[int]
    accountMembershipStatus: Optional[int]
    isGlobal: Optional[bool]
    avatarFrameId: Optional[str]
    reputation: Optional[int]
    postsCount: Optional[int]
    avatarFrame: Optional[AvatarFrame]
    membersCount: Optional[int]
    nickname: Optional[str]
    mediaList: Any
    icon: Optional[str]
    isNicknameVerified: Optional[bool]
    mood: Any
    level: Optional[int]
    notificationSubscriptionStatus: Optional[int]
    pushEnabled: Optional[bool]
    membershipStatus: Optional[int]
    content: Any
    joinedCount: Optional[int]
    role: Optional[int]
    commentsCount: Optional[int]
    aminoId: Optional[str]
    ndcId: Optional[int]
    createdTime: Optional[str]
    userProfileExtensions: Optional[UserProfileExtensions]
    storiesCount: Optional[int]
    blogsCount: Optional[int]


class DeviceInfo(BaseModel):
    lastClientType: Optional[int]


class AdvancedSettings(BaseModel):
    analyticsEnabled: Optional[int]


class AccountExtensions(BaseModel):
    adsFlags: Optional[int]


class Account(BaseModel):
    adsLevel: Optional[int]
    deviceInfo: Optional[DeviceInfo]
    mediaLabAdsMigrationJuly2020: Optional[bool]
    avatarFrameId: Optional[str]
    mediaLabAdsMigrationAugust2020: Optional[bool]
    adsEnabled: Optional[bool]

    username: Any
    status: Optional[int]
    uid: Optional[str]
    modifiedTime: Optional[str]
    twitterID: Any
    activation: Optional[int]
    phoneNumberActivation: Optional[int]
    emailActivation: Optional[int]
    appleID: Any
    facebookID: Any
    nickname: Optional[str]
    mediaList: Any
    googleID: Any
    icon: Optional[str]
    securityLevel: Optional[int]
    phoneNumber: Optional[str]
    membership: Any
    advancedSettings: Optional[AdvancedSettings]
    role: Optional[int]
    aminoIdEditable: Optional[bool]
    aminoId: Optional[str]
    createdTime: Optional[str]
    extensions: Optional[AccountExtensions]
    email: Optional[str]


class Login(BaseModel):
    auid: Optional[str]
    account: Optional[Account]
    secret: Optional[str]
    apiMessage: Optional[str] = Field(alias='api:message')
    sid: Optional[str]
    apiStatuscode: Optional[int] = Field(alias='api:statuscode')
    apiDuration: Optional[str] = Field(alias='api:duration')
    apiTimestamp: Optional[str] = Field(alias='api:timestamp')
    userProfile: Optional[UserProfile]


class LinkInfo(BaseModel):
    objectId: Optional[str]
    targetCode: Optional[int]
    ndcId: Optional[int]
    fullPath: Any
    shortCode: Any
    objectType: Optional[int]
    shareURLShortCode: Optional[str]
    targetCode: Optional[int]
    ndcId: Optional[int]
    fullPath: Optional[str]
    shareURLFullPath: Optional[str]


class Agent(BaseModel):
    status: Any
    ndcId: Any
    membersCount: Optional[int]
    icon: Any
    uid: Optional[str]
    followingStatus: Optional[int]
    level: Optional[int]
    nickname: Any
    isNicknameVerified: Optional[bool]
    accountMembershipStatus: Optional[int]
    membershipStatus: Optional[int]
    isGlobal: Optional[bool]
    reputation: Optional[int]
    role: Any


class Ranking(BaseModel):
    leaderboardEnabled: Optional[bool]
    rankingTable: Optional[Tuple]
    defaultLeaderboardType: Optional[int]
    leaderboardList: Optional[Tuple]
    enabled: Optional[bool]


class Influencer(BaseModel):
    maxVipNumbers: Optional[int]
    enabled: Optional[bool]
    maxVipMonthlyFee: Optional[int]
    minVipMonthlyFee: Optional[int]
    lock: Optional[bool]


class PublicChatPrivilege(BaseModel):
    minLevel: Optional[int]
    type: Optional[int]


class PublicChat(BaseModel):
    publicChatPrivilege: Optional[PublicChatPrivilege]
    enabled: Optional[bool]


class AvChat(BaseModel):
    screeningRoomEnabled: Optional[bool]
    audioEnabled: Optional[bool]
    videoEnabled: Optional[bool]
    audio2Enabled: Optional[bool]


class ModuleChat(BaseModel):
    enabled: Optional[bool]
    spamProtectionEnabled: Optional[bool]
    avChat: Optional[AvChat]
    publicChat: Optional[PublicChat]


class TopicCategories(BaseModel):
    enabled: Optional[bool]


class Featured(BaseModel):
    layout: Optional[int]
    publicChatRoomEnabled: Optional[bool]
    memberEnabled: Optional[bool]
    enabled: Optional[bool]
    lockMember: Optional[bool]
    postEnabled: Optional[bool]


class CatalogPrivilege(BaseModel):
    type: Optional[int]


class Catalog(BaseModel):
    curationEnabled: Optional[bool]
    catalogPrivilege: Optional[CatalogPrivilege]
    enabled: Optional[bool]


class UploadPrivilege(BaseModel):
    type: Optional[int]
    minLevel: Optional[int]


class AlbumManagePrivilege(BaseModel):
    type: Optional[int]
    minLevel: Optional[int]


class SharedFolder(BaseModel):
    enabled: Optional[bool]
    albumManagePrivilege: Optional[AlbumManagePrivilege]
    uploadPrivilege: Optional[UploadPrivilege]


class ExternalContent(BaseModel):
    enabled: Optional[bool]


class PollPrivilege(BaseModel):
    type: Optional[int]


class Poll(BaseModel):
    pollPrivilege: Optional[PollPrivilege]
    enabled: Optional[bool]


class LiveModePrivilege(BaseModel):
    minLevel: Optional[int]
    type: Optional[int]


class LiveMode(BaseModel):
    liveModePrivilege: Optional[LiveModePrivilege]
    enabled: Optional[bool]


class QuizPrivilege(BaseModel):
    type: Optional[int]


class Quiz(BaseModel):
    enabled: Optional[bool]
    quizPrivilege: Optional[QuizPrivilege]


class StoryPrivilege(BaseModel):
    type: Optional[int]


class Story(BaseModel):
    enabled: Optional[bool]
    storyPrivilege: Optional[StoryPrivilege]


class PublicChatRoomsPrivilege(BaseModel):
    type: Optional[int]
    minLevel: Optional[int]


class PublicChatRooms(BaseModel):
    publicChatRoomsPrivilege: Optional[PublicChatRoomsPrivilege]
    enabled: Optional[bool]


class CatalogEntryPrivilege(BaseModel):
    type: Optional[int]


class CatalogEntry(BaseModel):
    catalogEntryPrivilege: Optional[CatalogEntryPrivilege]
    enabled: Optional[bool]


class BlogPrivilege(BaseModel):
    type: Optional[int]


class TipCustomOption(BaseModel):
    value: Any
    icon: Optional[str]


class TipOptionList(BaseModel):
    value: Optional[int]
    icon: Optional[str]


class BlogExtensionsStyle(BaseModel):
    backgroundColor: Optional[str]


class BlogExtensions(BaseModel):
    style: Optional[BlogExtensionsStyle]
    fansOnly: Optional[bool]


class TipInfo(BaseModel):
    tipOptionList: Optional[Tuple[TipOptionList, ...]]
    tipMaxCoin: Optional[int]
    tippersCount: Optional[int]
    tippable: Optional[bool]
    tipMinCoin: Optional[int]
    tipCustomOption: Optional[TipCustomOption]
    tippedCoins: Optional[int]


class Blog(BaseModel):
    globalVotesCount: Optional[int]
    globalVotedValue: Optional[int]
    votedValue: Optional[int]
    keywords: Optional[str]
    strategyInfo: Optional[str]
    mediaList: Optional[Tuple]
    style: Optional[int]
    totalQuizPlayCount: Optional[int]
    title: Optional[str]
    tipInfo: Optional[TipInfo]
    contentRating: Optional[int]
    content: Optional[str]
    needHidden: Optional[bool]
    guestVotesCount: Optional[int]
    type: Optional[int]
    status: Optional[int]
    globalCommentsCount: Optional[int]
    modifiedTime: Optional[str]
    widgetDisplayInterval: Any
    totalPollVoteCount: Optional[int]
    blogId: Optional[str]
    viewCount: Optional[int]
    author: Optional[Author]
    extensions: Optional[BlogExtensions]
    votesCount: Optional[int]
    ndcId: Optional[int]
    createdTime: Optional[str]
    endTime: Any
    commentsCount: Optional[int]


class ScreeningRoomPrivilege(BaseModel):
    minLevel: Optional[int]
    type: Optional[int]


class ScreeningRoom(BaseModel):
    screeningRoomPrivilege: Optional[ScreeningRoomPrivilege]
    enabled: Optional[bool]


class QuestionPrivilege(BaseModel):
    type: Optional[int]


class Question(BaseModel):
    enabled: Optional[bool]
    questionPrivilege: Optional[QuestionPrivilege]


class WebLinkPrivilege(BaseModel):
    type: Optional[int]


class WebLink(BaseModel):
    webLinkPrivilege: Optional[WebLinkPrivilege]
    enabled: Optional[bool]


class Privilege(BaseModel):
    type: Optional[int]


class Image(BaseModel):
    enabled: Optional[bool]
    privilege: Optional[Privilege]


class PostType(BaseModel):
    image: Optional[Image]
    webLink: Optional[WebLink]
    question: Optional[Question]
    screeningRoom: Optional[ScreeningRoom]
    blog: Optional[Blog]
    catalogEntry: Optional[CatalogEntry]
    publicChatRooms: Optional[PublicChatRooms]
    story: Optional[Story]
    quiz: Optional[Quiz]
    liveMode: Optional[LiveMode]
    poll: Optional[Poll]


class Post(BaseModel):
    postType: Optional[PostType]
    enabled: Optional[bool]


class Module(BaseModel):
    post: Optional[Post]
    externalContent: Optional[ExternalContent]
    sharedFolder: Optional[SharedFolder]
    catalog: Optional[Catalog]
    featured: Optional[Featured]
    topicCategories: Optional[TopicCategories]
    chat: Optional[ModuleChat]
    influencer: Optional[Influencer]
    ranking: Optional[Ranking]


class CustomList(BaseModel):
    url: Optional[str]
    alias: Optional[str]
    id: Optional[str]


class Page(BaseModel):
    customList: Optional[Tuple[CustomList, ...]]
    defaultList: Optional[Tuple]


class Level1(BaseModel):
    id: Optional[str]


class Level2(BaseModel):
    id: Optional[str]


class LeftSidePanelNavigation(BaseModel):
    level2: Optional[Tuple[Level2, ...]]
    level1: Optional[Tuple[Level1, ...]]


class Style(BaseModel):
    iconColor: Any


class LeftSidePanel(BaseModel):
    style: Optional[Style]
    leftSidePanelNavigation: Optional[LeftSidePanelNavigation]


class HomePage(BaseModel):
    navigation: Optional[Tuple]


class Appearance(BaseModel):
    homePage: Optional[HomePage]
    leftSidePanel: Optional[LeftSidePanel]


class WelcomeMessage(BaseModel):
    text: Any
    enabled: Any


class General(BaseModel):
    premiumFeatureEnabled: Optional[bool]
    accountMembershipEnabled: Optional[bool]
    disableLiveLayerVisible: Optional[bool]
    onlyAllowOfficialTag: Optional[bool]
    welcomeMessage: Optional[WelcomeMessage]
    facebookAppIdList: Any
    videoUploadPolicy: Optional[int]
    invitePermission: Optional[int]
    disableLiveLayerActive: Optional[bool]
    joinedTopicIdList: Optional[Tuple]
    joinedBaselineCollectionIdList: Optional[Tuple]
    disableLocation: Optional[bool]
    hasPendingReviewRequest: Optional[bool]


class Configuration(BaseModel):
    general: Optional[General]
    appearance: Optional[Appearance]
    page: Optional[Page]
    module: Optional[Module]


class ThemePack(BaseModel):
    themePackRevision: Optional[int]
    themePackUrl: Optional[str]
    themeColor: Optional[str]
    themePackHash: Optional[str]


class CommunityAdvancedSettings(BaseModel):
    rankingTable: Optional[Tuple]
    leaderboardStyle: Optional[Dict]
    catalogEnabled: Optional[bool]
    joinedBaselineCollectionIdList: Optional[Tuple]
    defaultRankingTypeInLeaderboard: Optional[int]
    newsfeedPages: Optional[Tuple]
    hasPendingReviewRequest: Optional[bool]
    welcomeMessageEnabled: Any
    facebookAppIdList: Any
    frontPageLayout: Optional[int]
    pollMinFullBarVoteCount: Optional[int]
    welcomeMessageText: Any


class Community(BaseModel):
    probationStatus: Optional[int]
    keywords: Any
    themePack: Optional[ThemePack]
    listedStatus: Optional[int]
    endpoint: Optional[str]
    userAddedTopicList: Any
    templateId: Optional[int]
    joinType: Optional[int]
    searchable: Optional[bool]
    advancedSettings: Optional[CommunityAdvancedSettings]
    promotionalMediaList: Any
    ndcId: Optional[int]
    membersCount: Optional[int]
    activeInfo: Optional[Dict]
    configuration: Optional[Configuration]
    agent: Optional[Agent]
    extensions: Any
    createdTime: Optional[str]
    mediaList: Any
    name: Optional[str]
    primaryLanguage: Optional[str]
    isStandaloneAppMonetizationEnabled: Optional[bool]
    icon: Optional[str]
    isStandaloneAppDeprecated: Optional[bool]
    tagline: Optional[str]
    content: Any
    communityHeat: Optional[int]
    link: Optional[str]
    modifiedTime: Optional[str]
    status: Optional[int]


class LinkInfoExtensions(BaseModel):
    community: Optional[Community]
    linkInfo: Optional[LinkInfo]


class LinkInfoV2(BaseModel):
    path: Optional[str]
    extensions: Optional[LinkInfoExtensions]


class BaseLinkInfo(BaseModel):
    apiStatuscode: Optional[int] = Field(alias='api:statuscode')
    apiDuration: Optional[str] = Field(alias='api:duration')
    apiMessage: Optional[str] = Field(alias='api:message')
    linkInfoV2: Optional[LinkInfoV2]
    apiTimestamp: Optional[str] = Field(alias='api:timestamp')


class ChatExtensions(BaseModel):
    viewOnly: Optional[bool]
    coHost: Optional[Tuple[str, ...]]
    membersCanInvite: Optional[bool]
    language: Optional[str]
    bm: Optional[Tuple]
    lastMembersSummaryUpdateTime: Optional[int]
    fansOnly: Optional[bool]
    channelType: Optional[int]
    creatorUid: Optional[str] = Field(alias="uid")
    visibility: Optional[int]
    bannedMemberUidList: Optional[List[str]]
    announcement: Optional[str]
    pinAnnouncement: Optional[bool]
    vvChatJoinType: Optional[int]


class LastMessageSummary(BaseModel):
    uid: Optional[str]
    type: Optional[int]
    mediaType: Optional[int]
    content: Optional[str]
    messageId: Optional[str]
    createdTime: Optional[str]
    isHidden: Optional[bool]
    mediaValue: Any


class MembersSummary(BaseModel):
    status: Optional[int]
    uid: Optional[str]
    membershipStatus: Optional[int]
    role: Optional[int]
    nickname: Optional[str]
    icon: Optional[str]


class Chat(BaseModel):
    userAddedTopicList: Optional[Tuple]
    uid: Optional[str]
    membersQuota: Optional[int]
    membersSummary: Optional[Tuple[MembersSummary, ...]]
    threadId: Optional[str]
    keywords: Any
    membersCount: Optional[int]
    strategyInfo: Optional[str]
    isPinned: Optional[bool]
    title: Optional[str]
    membershipStatus: Optional[int]
    content: Optional[str]
    needHidden: Optional[bool]
    alertOption: Optional[int]
    lastReadTime: Optional[str]
    type: Optional[int]
    status: Optional[int]
    publishToGlobal: Optional[int]
    modifiedTime: Any
    lastMessageSummary: Optional[LastMessageSummary]
    condition: Optional[int]
    icon: Optional[str]
    latestActivityTime: Optional[str]
    author: Optional[Author]
    extensions: Optional[ChatExtensions]
    ndcId: Optional[int]
    createdTime: Any


class ChatBubble(BaseModel):
    id: str = Field(alias='bubbleId')
    resourceUrl: str
    config: Dict
    color: str = None
    isNew: bool
    md5: str


class Template(BaseModel):
    backgroundMedia: Tuple
    color: str
    config: Dict
    materialUrl: str
    name: str
    com_id: int = Field(alias='ndcId')
    id: str = Field(alias='templateId')


class Mention(BaseModel):
    uid: str


class Message(BaseModel):
    author: Optional[Author]
    mediaValue: Optional[str]
    threadId: Optional[str]
    mediaType: Optional[int]
    clientRefId: Optional[int]
    messageId: Optional[str]
    uid: Optional[str]
    createdTime: Optional[str]
    type: Optional[int]
    isHidden: Optional[bool]
    includedInSummary: Optional[bool]
    chatBubbleId: Optional[str]
    chatBubbleVersion: Optional[int]
    extensions: Optional[Extensions]
    ndcId: Optional[int]
    content: Optional[str]
    chatBubble: Optional[ChatBubble]


class Extensions(BaseModel):
    replyMessageId: Optional[str]
    replyMessage: Optional[Message]
    mentionedArray: Optional[Tuple[Mention, ...]]


class Paging(BaseModel):
    nextPageToken: Optional[str]
    prevPageToken: Optional[str]


class Messages(BaseModel):
    messageList: Optional[Tuple[Message, ...]]
    paging: Optional[Paging]
    apiMessage: Optional[str] = Field(alias='api:message')
    apiStatuscode: Optional[int] = Field(alias='api:statuscode')
    apiDuration: Optional[str] = Field(alias='api:duration')
    apiTimestamp: Optional[str] = Field(alias='api:timestamp')


class WalletInfo(BaseModel):
    adsEnabled: Optional[bool]
    adsFlags: Optional[int]
    adsVideoStats: Optional[int]
    businessCoinsEnabled: Optional[bool]
    totalBusinessCoins: Optional[int]
    totalBusinessCoinsFloat: Optional[float]
    totalCoins: Optional[int]
    totalCoinsFloat: Optional[float]


class O(BaseModel):
    ndcId: Optional[int]
    chatMessage: Optional[Message]
    alertOption: Optional[int]
    membershipStatus: Optional[int]
    channelKey: Optional[str]
    channelName: Optional[str]

    channelUid: Optional[int]
    expiredTime: Optional[int]
    ndcId: Optional[int]
    threadId: Optional[str]
    id: Optional[str]


class SocketAnswer(BaseModel):
    t: Optional[int]
    o: Optional[O]


class Wiki(BaseModel):
    globalVotesCount: Optional[int]
    globalVotedValue: Optional[int]
    votedValue: Optional[int]
    keywords: Optional[Any]
    mediaList: Optional[Any]
    style: Optional[int]
    author: Optional[Author]
    tipInfo: Optional[TipInfo]
    contentRating: Optional[int]
    label: Optional[str]
    content: Optional[str]
    needHidden: Optional[bool]
    guestVotesCount: Optional[int]
    status: Optional[int]
    globalCommentsCount: Optional[int]
    modifiedTime: Optional[str]
    itemId: Optional[str]
    extensions: Optional[Any]
    votesCount: Optional[int]
    ndcId: Optional[int]
    createdTime: Optional[str]
    commentsCount: Optional[int]


Message.update_forward_refs()
