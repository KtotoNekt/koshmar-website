const toolsBox = $(".tools-box")
const contentLoad = toolsBox.find(".load-content")
const textLoad = contentLoad.find("p")


const innterHtmlSuplCardLi = `
<div class="card">
    <div class="card-header">
        <div class="banner"></div>
    </div>
    <div class="card-body">
        <div class="profile-header">
            <div class="profil-logo">
                <img>
            </div>
            <div class="username">

            </div>
            <p class="username_foot"></p>
        </div>  
    </div>
    <a class="btn" target="_blank">Get Messages</a>
</div>`


function bannerSettings(bannerDiv, user) {
    $(bannerDiv).removeAttr("class");
    const bannerUrl = user.banner_url

    if (bannerUrl || user.banner) {
        if (!bannerUrl) {
            bannerUrl = `https://cdn.discordapp.com/banners/${user.id}/${user.banner}?size=512`
        }
        $(bannerDiv).attr({
            class: "banner-img",
            style: `background: url(${bannerUrl})`,
            "data-darkreader-inline-bgcolor": "",
            "--darkreader-inline-bgcolor": "rgba(0, 0, 0, 0)"
        });
    } else {
        $(bannerDiv).attr({
            class: "banner",
            style: `background-color: ${user.banner_color}`
        })
    }
}

function usernameSettings(userNameDiv, userInfo) {
    const userGlobalName = userInfo.global_name
    const userUsername = userInfo.username

    if (userGlobalName) {
        userNameDiv.text(userGlobalName)
    } else {
        userNameDiv.text(userUsername)
    }

    const userDiscriminator = userInfo.discriminator
    if (userDiscriminator != "0") {
        const discriminatorSpan = document.createElement("span")
        discriminatorSpan.textContent = "#" + userDiscriminator
        userNameDiv.append(discriminatorSpan)
    }
}

function initSlider(objects, divClass, funcSetSuplInfo) {
    $(`.${divClass}`).parent().css("visibility", "visible")

    let position
    if (Object.keys(objects).length == 1) {
        position = 1
    } else {
        position = 0
    }

    $(`.${divClass} .slider`)[0].innerHTML = ''
    

    for (const object of objects) {
        const li = $("<li class='slider--item'></li>").appendTo(`.${divClass} .slider`)

        if (position === 0) {
            li.addClass("slider--item-left")
            position = 1;
        } else if (position === 1) {
            li.addClass("slider--item-center")
            position = 2
        } else if (position === 2) {
            li.addClass("slider--item-right")
            position = 3
        }

        li[0].innerHTML = innterHtmlSuplCardLi
        li.find(".card-header div").css("background-color", "black")

        funcSetSuplInfo(li, object)
    }
}

function settingUserMiniCard(li, friendUser) {
    li.find(".btn").attr("href", "/api/get/messages/"+friendUser.id+"?referer=friends")
    li.find(".profil-logo").click(() => {
        window.open(`/api/get/${friendUser.id}/card`, '_blank')
    })

    let url
    if (friendUser.avatar) {
        url = `https://cdn.discordapp.com/avatars/${friendUser.id}/${friendUser.avatar}`
    } else {
        let index;
        if (friendUser.discriminator === "0") {
            index = (friendUser.id >> 22) % 6
        } else {
            index = friendUser.discriminator % 5
        }

        url = `https://cdn.discordapp.com/embed/avatars/${index}.png`
    }


    li.find(".profil-logo img").attr("src", url)

    const userNameDiv = li.find(".username")
    usernameSettings(userNameDiv, friendUser)

    li.find(".username_foot").text(friendUser.username)
}


function friendsSlider(friends) {
    initSlider(friends, "friends", (li, friend) => {
        settingUserMiniCard(li, friend.user)
    })
}

function dmChannelsSlider(dmChannels) {
    initSlider(dmChannels, "dm-channels", (li, dmChannel) => {
        switch (dmChannel.type) {
            case 1:
                settingUserMiniCard(li, dmChannel.recipients[0])
                break
            case 3:
                li.find(".btn").attr("href", "/api/get/messages/"+dmChannel.id+"?referer=channel")

                if (dmChannel.name) {
                    li.find(".username").text(dmChannel.name)
                } else {
                    li.find(".username").text("Группа")
                }

                let recipients = ""
                for (const recipient of dmChannel.recipients) {
                    recipients += recipient.global_name ?? recipient.username
                    recipients += ", "
                    
                    if (recipients.length > 74) {
                        recipients = recipients.slice(0, 74)
                        recipients += "..."
                        break
                    }
                }

                li.find(".username_foot").text(recipients)

                li.find(".profil-logo img").attr("src", dmChannel.icon ? `https://cdn.discordapp.com/channel-icons/${dmChannel.id}/${dmChannel.icon}.png` : "https://discordapp.com/assets/485a854d5171c8dc98088041626e6fea.png")

                break
        }
    })
}

function guildsSlider(guilds) {
    initSlider(guilds, "guilds", (li, guild) => {
        li.find(".btn").attr("href", "/api/get/guild")
        li.find(".btn").text("Get Info")
        li.find(".username").text(guild.name)
        li.find(".username_foot").text(guild.owner ? "Владелец сервера" : "Участник сервера")
        li.find(".profil-logo img").attr("src", guild.icon ? `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png` : "")
    })
}


function createUserProfileCard(profile) {
    $(toolsBox).find(".card-about").attr("style", "visibility: visible")

    const userInfo = profile.bot ? profile : profile.user

    const bannerDiv = $(toolsBox).find(".card-about .card-header div")
    bannerSettings(bannerDiv, userInfo)

    $(toolsBox).find(".card-about .profil-logo img").attr("src", userInfo.avatar_url)

    const badgesDivContainer = $(toolsBox).find(".card-about .badges-container")
    badgesDivContainer.innerHTML = ''

    for (const badge of profile.badges) {
        const div = document.createElement("div")
        const img = document.createElement("img")
        const divToolTip = document.createElement("div")

        div.classList.add("badge-item")
        img.src = badge.icon_url
        divToolTip.classList.add("tooltip")
        divToolTip.classList.add("tooltip-up")
        divToolTip.textContent = badge.description
        
        div.appendChild(img)
        div.appendChild(divToolTip)

        badgesDivContainer.append(div)
    }

    const userNameDiv = $(toolsBox).find(".card-about .username")
    usernameSettings(userNameDiv, userInfo)

    $(toolsBox).find(".card-about .username_foot").text(userInfo.username)
    if (!userInfo.bot)
        $(toolsBox).find(".card-about .pronouns").text(userInfo.pronouns)

    const basicInfos = $(toolsBox).find(".card-about .basic-infos > p")
    basicInfos[0].innerHTML = userInfo.bio
    basicInfos[1].textContent = userInfo.creation_date
    basicInfos[2].textContent = profile.email
    basicInfos[3].textContent = profile.phone
    basicInfos[4].textContent = profile.locale
}

function preInitSliders(array, divID, func) {
    if (array.length) {
        $(`#${divID}`).css("display", "block")
        func(array)
    }
    else
        $(`#${divID}`).css("display", "none")
}
