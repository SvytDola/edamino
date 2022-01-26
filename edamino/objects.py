import pydantic
import typing


class UserProfileExtensions(pydantic.BaseModel):
    privilegeOfCommentOnUserProfile: typing.Optional[int]
    customTitles: typing.Optional[typing.Tuple]


class AvatarFrame(pydantic.BaseModel):
    status: typing.Optional[int]
    ownershipStatus: typing.Any
    version: typing.Optional[int]
    resourceUrl: typing.Optional[str]
    name: typing.Optional[str]
    icon: typing.Optional[str]
    frameType: typing.Optional[int]
    frameId: typing.Optional[str]


class Author(pydantic.BaseModel):
    status: typing.Optional[int]
    isNicknameVerified: typing.Optional[bool]
    uid: typing.Optional[str]
    level: typing.Optional[int]
    followingStatus: typing.Optional[int]
    accountMembershipStatus: typing.Optional[int]
    isGlobal: typing.Optional[bool]
    membershipStatus: typing.Optional[int]
    reputation: typing.Optional[int]
    role: typing.Optional[int]
    ndcId: typing.Optional[int]
    membersCount: typing.Optional[int]
    nickname: typing.Optional[str]
    icon: typing.Optional[str]
    avatarFrame: typing.Optional[AvatarFrame]


class UserProfile(pydantic.BaseModel):
    status: typing.Optional[int]
    moodSticker: typing.Any
    itemsCount: typing.Optional[int]
    consecutiveCheckInDays: typing.Any
    uid: typing.Optional[str]
    modifiedTime: typing.Optional[str]
    followingStatus: typing.Optional[int]
    onlineStatus: typing.Optional[int]
    accountMembershipStatus: typing.Optional[int]
    isGlobal: typing.Optional[bool]
    avatarFrameId: typing.Optional[str]
    reputation: typing.Optional[int]
    postsCount: typing.Optional[int]
    avatarFrame: typing.Optional[AvatarFrame]
    membersCount: typing.Optional[int]
    nickname: typing.Optional[str]
    mediaList: typing.Any
    icon: typing.Optional[str]
    isNicknameVerified: typing.Optional[bool]
    mood: typing.Any
    level: typing.Optional[int]
    notificationSubscriptionStatus: typing.Optional[int]
    pushEnabled: typing.Optional[bool]
    membershipStatus: typing.Optional[int]
    content: typing.Any
    joinedCount: typing.Optional[int]
    role: typing.Optional[int]
    commentsCount: typing.Optional[int]
    aminoId: typing.Optional[str]
    ndcId: typing.Optional[int]
    createdTime: typing.Optional[str]
    userProfileExtensions: typing.Optional[UserProfileExtensions]
    storiesCount: typing.Optional[int]
    blogsCount: typing.Optional[int]


class DeviceInfo(pydantic.BaseModel):
    lastClientType: typing.Optional[int]


class AdvancedSettings(pydantic.BaseModel):
    analyticsEnabled: typing.Optional[int]


class AccountExtensions(pydantic.BaseModel):
    adsFlags: typing.Optional[int]


class Account(pydantic.BaseModel):
    adsLevel: typing.Optional[int]
    deviceInfo: typing.Optional[DeviceInfo]
    mediaLabAdsMigrationJuly2020: typing.Optional[bool]
    avatarFrameId: typing.Optional[str]
    mediaLabAdsMigrationAugust2020: typing.Optional[bool]
    adsEnabled: typing.Optional[bool]

    username: typing.Any
    status: typing.Optional[int]
    uid: typing.Optional[str]
    modifiedTime: typing.Optional[str]
    twitterID: typing.Any
    activation: typing.Optional[int]
    phoneNumberActivation: typing.Optional[int]
    emailActivation: typing.Optional[int]
    appleID: typing.Any
    facebookID: typing.Any
    nickname: typing.Optional[str]
    mediaList: typing.Any
    googleID: typing.Any
    icon: typing.Optional[str]
    securityLevel: typing.Optional[int]
    phoneNumber: typing.Optional[str]
    membership: typing.Any
    advancedSettings: typing.Optional[AdvancedSettings]
    role: typing.Optional[int]
    aminoIdEditable: typing.Optional[bool]
    aminoId: typing.Optional[str]
    createdTime: typing.Optional[str]
    extensions: typing.Optional[AccountExtensions]
    email: typing.Optional[str]


class Login(pydantic.BaseModel):
    auid: typing.Optional[str]
    account: typing.Optional[Account]
    secret: typing.Optional[str]
    apiMessage: typing.Optional[str] = pydantic.Field(alias='api:message')
    sid: typing.Optional[str]
    apiStatuscode: typing.Optional[int] = pydantic.Field(alias='api:statuscode')
    apiDuration: typing.Optional[str] = pydantic.Field(alias='api:duration')
    apiTimestamp: typing.Optional[str] = pydantic.Field(alias='api:timestamp')
    userProfile: typing.Optional[UserProfile]


class LinkInfo(pydantic.BaseModel):
    objectId: typing.Optional[str]
    targetCode: typing.Optional[int]
    ndcId: typing.Optional[int]
    fullPath: typing.Any
    shortCode: typing.Any
    objectType: typing.Optional[int]
    shareURLShortCode: typing.Optional[str]
    targetCode: typing.Optional[int]
    ndcId: typing.Optional[int]
    fullPath: typing.Optional[str]
    shareURLFullPath: typing.Optional[str]


class Agent(pydantic.BaseModel):
    status: typing.Any
    ndcId: typing.Any
    membersCount: typing.Optional[int]
    icon: typing.Any
    uid: typing.Optional[str]
    followingStatus: typing.Optional[int]
    level: typing.Optional[int]
    nickname: typing.Any
    isNicknameVerified: typing.Optional[bool]
    accountMembershipStatus: typing.Optional[int]
    membershipStatus: typing.Optional[int]
    isGlobal: typing.Optional[bool]
    reputation: typing.Optional[int]
    role: typing.Any


class Ranking(pydantic.BaseModel):
    leaderboardEnabled: typing.Optional[bool]
    rankingTable: typing.Optional[typing.Tuple]
    defaultLeaderboardType: typing.Optional[int]
    leaderboardList: typing.Optional[typing.Tuple]
    enabled: typing.Optional[bool]


class Influencer(pydantic.BaseModel):
    maxVipNumbers: typing.Optional[int]
    enabled: typing.Optional[bool]
    maxVipMonthlyFee: typing.Optional[int]
    minVipMonthlyFee: typing.Optional[int]
    lock: typing.Optional[bool]


class PublicChatPrivilege(pydantic.BaseModel):
    minLevel: typing.Optional[int]
    type: typing.Optional[int]


class PublicChat(pydantic.BaseModel):
    publicChatPrivilege: typing.Optional[PublicChatPrivilege]
    enabled: typing.Optional[bool]


class AvChat(pydantic.BaseModel):
    screeningRoomEnabled: typing.Optional[bool]
    audioEnabled: typing.Optional[bool]
    videoEnabled: typing.Optional[bool]
    audio2Enabled: typing.Optional[bool]


class ModuleChat(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    spamProtectionEnabled: typing.Optional[bool]
    avChat: typing.Optional[AvChat]
    publicChat: typing.Optional[PublicChat]


class TopicCategories(pydantic.BaseModel):
    enabled: typing.Optional[bool]


class Featured(pydantic.BaseModel):
    layout: typing.Optional[int]
    publicChatRoomEnabled: typing.Optional[bool]
    memberEnabled: typing.Optional[bool]
    enabled: typing.Optional[bool]
    lockMember: typing.Optional[bool]
    postEnabled: typing.Optional[bool]


class CatalogPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Catalog(pydantic.BaseModel):
    curationEnabled: typing.Optional[bool]
    catalogPrivilege: typing.Optional[CatalogPrivilege]
    enabled: typing.Optional[bool]


class UploadPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]
    minLevel: typing.Optional[int]


class AlbumManagePrivilege(pydantic.BaseModel):
    type: typing.Optional[int]
    minLevel: typing.Optional[int]


class SharedFolder(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    albumManagePrivilege: typing.Optional[AlbumManagePrivilege]
    uploadPrivilege: typing.Optional[UploadPrivilege]


class ExternalContent(pydantic.BaseModel):
    enabled: typing.Optional[bool]


class PollPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Poll(pydantic.BaseModel):
    pollPrivilege: typing.Optional[PollPrivilege]
    enabled: typing.Optional[bool]


class LiveModePrivilege(pydantic.BaseModel):
    minLevel: typing.Optional[int]
    type: typing.Optional[int]


class LiveMode(pydantic.BaseModel):
    liveModePrivilege: typing.Optional[LiveModePrivilege]
    enabled: typing.Optional[bool]


class QuizPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Quiz(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    quizPrivilege: typing.Optional[QuizPrivilege]


class StoryPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Story(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    storyPrivilege: typing.Optional[StoryPrivilege]


class PublicChatRoomsPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]
    minLevel: typing.Optional[int]


class PublicChatRooms(pydantic.BaseModel):
    publicChatRoomsPrivilege: typing.Optional[PublicChatRoomsPrivilege]
    enabled: typing.Optional[bool]


class CatalogEntryPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class CatalogEntry(pydantic.BaseModel):
    catalogEntryPrivilege: typing.Optional[CatalogEntryPrivilege]
    enabled: typing.Optional[bool]


class BlogPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class TipCustomOption(pydantic.BaseModel):
    value: typing.Any
    icon: typing.Optional[str]


class TipOptionList(pydantic.BaseModel):
    value: typing.Optional[int]
    icon: typing.Optional[str]


class TipInfo(pydantic.BaseModel):
    tipOptionList: typing.Optional[typing.Tuple[TipOptionList, ...]]
    tipMaxCoin: typing.Optional[int]
    tippersCount: typing.Optional[int]
    tippable: typing.Optional[bool]
    tipMinCoin: typing.Optional[int]
    tipCustomOption: typing.Optional[TipCustomOption]
    tippedCoins: typing.Optional[float]


class BlogExtensionsStyle(pydantic.BaseModel):
    backgroundColor: typing.Optional[str]


class BlogExtensions(pydantic.BaseModel):
    style: typing.Optional[BlogExtensionsStyle]
    fansOnly: typing.Optional[bool]


class Blog(pydantic.BaseModel):
    globalVotesCount: typing.Optional[int]
    globalVotedValue: typing.Optional[int]
    votedValue: typing.Optional[int]
    keywords: typing.Optional[str]
    strategyInfo: typing.Optional[str]
    mediaList: typing.Optional[typing.Tuple]
    style: typing.Optional[int]
    totalQuizPlayCount: typing.Optional[int]
    title: typing.Optional[str]
    tipInfo: typing.Optional[TipInfo]
    contentRating: typing.Optional[int]
    content: typing.Optional[str]
    needHidden: typing.Optional[bool]
    guestVotesCount: typing.Optional[int]
    type: typing.Optional[int]
    status: typing.Optional[int]
    globalCommentsCount: typing.Optional[int]
    modifiedTime: typing.Optional[str]
    widgetDisplayInterval: typing.Any
    totalPollVoteCount: typing.Optional[int]
    blogId: typing.Optional[str]
    viewCount: typing.Optional[int]
    author: typing.Optional[Author]
    extensions: typing.Optional[BlogExtensions]
    votesCount: typing.Optional[int]
    ndcId: typing.Optional[int]
    createdTime: typing.Optional[str]
    endTime: typing.Any
    commentsCount: typing.Optional[int]


class ScreeningRoomPrivilege(pydantic.BaseModel):
    minLevel: typing.Optional[int]
    type: typing.Optional[int]


class ScreeningRoom(pydantic.BaseModel):
    screeningRoomPrivilege: typing.Optional[ScreeningRoomPrivilege]
    enabled: typing.Optional[bool]


class QuestionPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Question(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    questionPrivilege: typing.Optional[QuestionPrivilege]


class WebLinkPrivilege(pydantic.BaseModel):
    type: typing.Optional[int]


class WebLink(pydantic.BaseModel):
    webLinkPrivilege: typing.Optional[WebLinkPrivilege]
    enabled: typing.Optional[bool]


class Privilege(pydantic.BaseModel):
    type: typing.Optional[int]


class Image(pydantic.BaseModel):
    enabled: typing.Optional[bool]
    privilege: typing.Optional[Privilege]


class PostType(pydantic.BaseModel):
    image: typing.Optional[Image]
    webLink: typing.Optional[WebLink]
    question: typing.Optional[Question]
    screeningRoom: typing.Optional[ScreeningRoom]
    blog: typing.Optional[Blog]
    catalogEntry: typing.Optional[CatalogEntry]
    publicChatRooms: typing.Optional[PublicChatRooms]
    story: typing.Optional[Story]
    quiz: typing.Optional[Quiz]
    liveMode: typing.Optional[LiveMode]
    poll: typing.Optional[Poll]


class Post(pydantic.BaseModel):
    postType: typing.Optional[PostType]
    enabled: typing.Optional[bool]


class Module(pydantic.BaseModel):
    post: typing.Optional[Post]
    externalContent: typing.Optional[ExternalContent]
    sharedFolder: typing.Optional[SharedFolder]
    catalog: typing.Optional[Catalog]
    featured: typing.Optional[Featured]
    topicCategories: typing.Optional[TopicCategories]
    chat: typing.Optional[ModuleChat]
    influencer: typing.Optional[Influencer]
    ranking: typing.Optional[Ranking]


class CustomList(pydantic.BaseModel):
    url: typing.Optional[str]
    alias: typing.Optional[str]
    id: typing.Optional[str]


class Page(pydantic.BaseModel):
    customList: typing.Optional[typing.Tuple[CustomList, ...]]
    defaultList: typing.Optional[typing.Tuple]


class Level1(pydantic.BaseModel):
    id: typing.Optional[str]


class Level2(pydantic.BaseModel):
    id: typing.Optional[str]


class LeftSidePanelNavigation(pydantic.BaseModel):
    level2: typing.Optional[typing.Tuple[Level2, ...]]
    level1: typing.Optional[typing.Tuple[Level1, ...]]


class Style(pydantic.BaseModel):
    iconColor: typing.Any


class LeftSidePanel(pydantic.BaseModel):
    style: typing.Optional[Style]
    leftSidePanelNavigation: typing.Optional[LeftSidePanelNavigation]


class HomePage(pydantic.BaseModel):
    navigation: typing.Optional[typing.Tuple]


class Appearance(pydantic.BaseModel):
    homePage: typing.Optional[HomePage]
    leftSidePanel: typing.Optional[LeftSidePanel]


class WelcomeMessage(pydantic.BaseModel):
    text: typing.Any
    enabled: typing.Any


class General(pydantic.BaseModel):
    premiumFeatureEnabled: typing.Optional[bool]
    accountMembershipEnabled: typing.Optional[bool]
    disableLiveLayerVisible: typing.Optional[bool]
    onlyAllowOfficialTag: typing.Optional[bool]
    welcomeMessage: typing.Optional[WelcomeMessage]
    facebookAppIdList: typing.Any
    videoUploadPolicy: typing.Optional[int]
    invitePermission: typing.Optional[int]
    disableLiveLayerActive: typing.Optional[bool]
    joinedTopicIdList: typing.Optional[typing.Tuple]
    joinedBaselineCollectionIdList: typing.Optional[typing.Tuple]
    disableLocation: typing.Optional[bool]
    hasPendingReviewRequest: typing.Optional[bool]


class Configuration(pydantic.BaseModel):
    general: typing.Optional[General]
    appearance: typing.Optional[Appearance]
    page: typing.Optional[Page]
    module: typing.Optional[Module]


class ThemePack(pydantic.BaseModel):
    themePackRevision: typing.Optional[int]
    themePackUrl: typing.Optional[str]
    themeColor: typing.Optional[str]
    themePackHash: typing.Optional[str]


class CommunityAdvancedSettings(pydantic.BaseModel):
    rankingTable: typing.Optional[typing.Tuple]
    leaderboardStyle: typing.Optional[typing.Dict]
    catalogEnabled: typing.Optional[bool]
    joinedBaselineCollectionIdList: typing.Optional[typing.Tuple]
    defaultRankingTypeInLeaderboard: typing.Optional[int]
    newsfeedPages: typing.Optional[typing.Tuple]
    hasPendingReviewRequest: typing.Optional[bool]
    welcomeMessageEnabled: typing.Any
    facebookAppIdList: typing.Any
    frontPageLayout: typing.Optional[int]
    pollMinFullBarVoteCount: typing.Optional[int]
    welcomeMessageText: typing.Any


class Community(pydantic.BaseModel):
    probationStatus: typing.Optional[int]
    keywords: typing.Any
    themePack: typing.Optional[ThemePack]
    listedStatus: typing.Optional[int]
    endpoint: typing.Optional[str]
    userAddedTopicList: typing.Any
    templateId: typing.Optional[int]
    joinType: typing.Optional[int]
    searchable: typing.Optional[bool]
    advancedSettings: typing.Optional[CommunityAdvancedSettings]
    promotionalMediaList: typing.Any
    ndcId: typing.Optional[int]
    membersCount: typing.Optional[int]
    activeInfo: typing.Optional[typing.Dict]
    configuration: typing.Optional[Configuration]
    agent: typing.Optional[Agent]
    extensions: typing.Any
    createdTime: typing.Optional[str]
    mediaList: typing.Any
    name: typing.Optional[str]
    primaryLanguage: typing.Optional[str]
    isStandaloneAppMonetizationEnabled: typing.Optional[bool]
    icon: typing.Optional[str]
    isStandaloneAppDeprecated: typing.Optional[bool]
    tagline: typing.Optional[str]
    content: typing.Any
    communityHeat: typing.Optional[int]
    link: typing.Optional[str]
    modifiedTime: typing.Optional[str]
    status: typing.Optional[int]


class LinkInfoExtensions(pydantic.BaseModel):
    community: typing.Optional[Community]
    linkInfo: typing.Optional[LinkInfo]


class LinkInfoV2(pydantic.BaseModel):
    path: typing.Optional[str]
    extensions: typing.Optional[LinkInfoExtensions]


class BaseLinkInfo(pydantic.BaseModel):
    apiStatuscode: typing.Optional[int] = pydantic.Field(alias='api:statuscode')
    apiDuration: typing.Optional[str] = pydantic.Field(alias='api:duration')
    apiMessage: typing.Optional[str] = pydantic.Field(alias='api:message')
    linkInfoV2: typing.Optional[LinkInfoV2]
    apiTimestamp: typing.Optional[str] = pydantic.Field(alias='api:timestamp')


class ChatExtensions(pydantic.BaseModel):
    viewOnly: typing.Optional[bool]
    coHost: typing.Optional[typing.Tuple[str, ...]]
    membersCanInvite: typing.Optional[bool]
    language: typing.Optional[str]
    bm: typing.Optional[typing.Tuple]
    lastMembersSummaryUpdateTime: typing.Optional[int]
    fansOnly: typing.Optional[bool]
    channelType: typing.Optional[int]


class LastMessageSummary(pydantic.BaseModel):
    uid: typing.Optional[str]
    type: typing.Optional[int]
    mediaType: typing.Optional[int]
    content: typing.Optional[str]
    messageId: typing.Optional[str]
    createdTime: typing.Optional[str]
    isHidden: typing.Optional[bool]
    mediaValue: typing.Any


class MembersSummary(pydantic.BaseModel):
    status: typing.Optional[int]
    uid: typing.Optional[str]
    membershipStatus: typing.Optional[int]
    role: typing.Optional[int]
    nickname: typing.Optional[str]
    icon: typing.Optional[str]


class Chat(pydantic.BaseModel):
    userAddedTopicList: typing.Optional[typing.Tuple]
    uid: typing.Optional[str]
    membersQuota: typing.Optional[int]
    membersSummary: typing.Optional[typing.Tuple[MembersSummary, ...]]
    threadId: typing.Optional[str]
    keywords: typing.Any
    membersCount: typing.Optional[int]
    strategyInfo: typing.Optional[str]
    isPinned: typing.Optional[bool]
    title: typing.Optional[str]
    membershipStatus: typing.Optional[int]
    content: typing.Optional[str]
    needHidden: typing.Optional[bool]
    alertOption: typing.Optional[int]
    lastReadTime: typing.Optional[str]
    type: typing.Optional[int]
    status: typing.Optional[int]
    publishToGlobal: typing.Optional[int]
    modifiedTime: typing.Any
    lastMessageSummary: typing.Optional[LastMessageSummary]
    condition: typing.Optional[int]
    icon: typing.Optional[str]
    latestActivityTime: typing.Optional[str]
    author: typing.Optional[Author]
    extensions: typing.Optional[ChatExtensions]
    ndcId: typing.Optional[int]
    createdTime: typing.Any


class ChatBubble(pydantic.BaseModel):
    id: str = pydantic.Field(alias='bubbleId')
    resourceUrl: str
    config: typing.Dict
    color: str = None
    isNew: bool
    md5: str


class Template(pydantic.BaseModel):
    backgroundMedia: typing.Tuple
    color: str
    config: typing.Dict
    materialUrl: str
    name: str
    com_id: int = pydantic.Field(alias='ndcId')
    id: str = pydantic.Field(alias='templateId')


class Message(pydantic.BaseModel):
    author: typing.Optional[Author]
    mediaValue: typing.Optional[str]
    threadId: typing.Optional[str]
    mediaType: typing.Optional[int]
    clientRefId: typing.Optional[int]
    messageId: typing.Optional[str]
    uid: typing.Optional[str]
    createdTime: typing.Optional[str]
    type: typing.Optional[int]
    isHidden: typing.Optional[bool]
    includedInSummary: typing.Optional[bool]
    chatBubbleId: typing.Optional[str]
    chatBubbleVersion: typing.Optional[int]
    extensions: typing.Optional[typing.Dict]
    ndcId: typing.Optional[int]
    content: typing.Optional[str]
    chatBubble: typing.Optional[ChatBubble]


class Paging(pydantic.BaseModel):
    nextPageToken: typing.Optional[str]
    prevPageToken: typing.Optional[str]


class Messages(pydantic.BaseModel):
    messageList: typing.Optional[typing.Tuple[Chat, ...]]
    paging: typing.Optional[Paging]
    apiMessage: typing.Optional[str] = pydantic.Field(alias='api:message')
    apiStatuscode: typing.Optional[int] = pydantic.Field(alias='api:statuscode')
    apiDuration: typing.Optional[str] = pydantic.Field(alias='api:duration')
    apiTimestamp: typing.Optional[str] = pydantic.Field(alias='api:timestamp')


class WalletInfo(pydantic.BaseModel):
    adsEnabled: typing.Optional[bool]
    adsFlags: typing.Optional[int]
    adsVideoStats: typing.Optional[int]
    businessCoinsEnabled: typing.Optional[bool]
    totalBusinessCoins: typing.Optional[int]
    totalBusinessCoinsFloat: typing.Optional[float]
    totalCoins: typing.Optional[int]
    totalCoinsFloat: typing.Optional[float]
